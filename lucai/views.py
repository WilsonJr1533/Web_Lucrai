from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Transacao
from .forms import TransacaoForm
import matplotlib.pyplot as plt
import mpld3
from threading import Thread




def home(request):
    return render(request, 'pages/home.html')




from django.http import JsonResponse
import google.generativeai as genai


def index(request):
    # ...


    # Verifica se há uma resposta da IA na variável de sessão
    resposta_ia = request.session.pop('resposta_ia', None)

    return render(request, 'pages/index.html', {'resposta_ia': resposta_ia})


def obter_resposta_ia(mensagem_usuario):
    
    genai.configure(api_key="API")
    
    

    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ]

    model = genai.GenerativeModel(
        model_name="gemini-pro", generation_config=generation_config, safety_settings=safety_settings
    )

    prompt_parts = [
        "vc é um consultor financeiro virtual chamado Luc, vc irá perguntar o que o usuário precisa de ajuda.\nSua função é ajudar o usuário com suas finanças, conforme solicitado pelo usuario\n  Perguntas referentes a valores que o usuário teria, vc responderá apenas o valor final",
        mensagem_usuario,
    ]

    response = model.generate_content(prompt_parts)
    return response.text

def obter_resposta_ia_view(request):
    if request.method == 'POST':
        mensagem_usuario = request.POST.get('mensagem_usuario', '')
        print(f'Mensagem do Usuário: {mensagem_usuario}')

        resposta_ia = obter_resposta_ia(mensagem_usuario)
        print(f'Resposta IA: {resposta_ia}')

        return JsonResponse({'resposta_ia': resposta_ia})
    else:
        return JsonResponse({'error': 'Método não permitido'})





# views.py

def grafico(request):
    try:
        if request.method == 'POST' and 'remover_transacoes' in request.POST:
            # Se o botão "Limpar Transações" for pressionado, remova todas as transações
            Transacao.objects.all().delete()
            return redirect('grafico')

        transacoes = Transacao.objects.all()
        transacoes = sorted(transacoes, key=lambda x: x.data)

        descricoes = [transacao.descricao for transacao in transacoes]
        valores = [float(transacao.valor) for transacao in transacoes]
        cores = ['green' if transacao.tipo == 'receita' else 'red' for transacao in transacoes]

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(range(len(descricoes)), valores, color=cores, width=0.4)

        total_despesas = sum(val for val, cor in zip(valores, cores) if cor == 'red')
        total_receitas = sum(val for val, cor in zip(valores, cores) if cor == 'green')

        deficit = total_receitas - total_despesas

        ax.text(-0.5, total_despesas + 1, f'Total Despesas: {total_despesas:.2f} R$', ha='left', va='bottom', color='red', bbox=dict(facecolor='lightgrey', edgecolor='none', boxstyle='round,pad=0.3'))
        ax.text(-0.5, total_receitas + 1, f'Total Receitas: {total_receitas:.2f} R$', ha='left', va='bottom', color='green', bbox=dict(facecolor='lightgrey', edgecolor='none', boxstyle='round,pad=0.3'))

        ax.set_xlabel('Transações')
        ax.set_ylabel('Valor (R$)')
        ax.set_title('Resumo Financeiro Mensal')

        plt.tight_layout()

        grafico_html = mpld3.fig_to_html(fig)
        grafico_id = mpld3.utils.get_id(fig)

        # Passando dados adicionais para o template
        grafico_data = {
            'grafico_id': grafico_id,
            'valores': valores,
            'total_despesas': total_despesas,
            'total_receitas': total_receitas,
            'deficit': deficit,
            'transacoes': [(transacao.descricao, float(transacao.valor)) for transacao in transacoes],
        }

        return render(request, 'pages/grafico.html', {'grafico_html': grafico_html, 'grafico_data': grafico_data, 'form': TransacaoForm()})
    except Exception as e:
        return render(request, 'pages/erro.html', {'erro': str(e)})



# ...

def adicionar_transacao(request):
    if request.method == 'POST':
        form = TransacaoForm(request.POST)
        if form.is_valid():
            nova_transacao = form.save(commit=False)
            
            # Verificar se já existe uma transação com a mesma descrição
            transacao_existente = Transacao.objects.filter(descricao=nova_transacao.descricao).first()
            
            if transacao_existente:
                # Se existir, adicione o valor à transação existente
                transacao_existente.valor += nova_transacao.valor
                transacao_existente.save()
            else:
                # Caso contrário, salve a nova transação
                nova_transacao.save()

            # Chame a função para obter a resposta da IA
            mensagem_usuario = f"Adicionada nova transação: {nova_transacao.descricao} - Valor: {nova_transacao.valor} R$"
            resposta_ia = obter_resposta_ia(mensagem_usuario)

            # Salve a resposta da IA na variável de sessão
            request.session['resposta_ia'] = resposta_ia

            return redirect('grafico')  # Redireciona para o dashboard
    else:
        form = TransacaoForm()

    return render(request, 'pages/adicionar_transacao.html', {'form': form})
