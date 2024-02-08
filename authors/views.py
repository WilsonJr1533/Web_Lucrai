from django.shortcuts import render, redirect
from django.http import Http404
from .forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from authors.models import CustomUser



# Resto do seu código...




def register(request):
    # Se houver dados de formulário na sessão, use-os para preencher o formulário
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(initial=register_form_data)
    
    if request.user.is_authenticated:
        # Redirecionar para o dashboard se já estiver autenticado
        return redirect('dashboard')
    
    return render(request, 'author/pages/register.html', {
        'form': form,
        'form_action': reverse('authors:register_create'),
    })

def register_create(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Use o manager personalizado para criar um usuário
            user = CustomUser.objects.create_user(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                cpf=form.cleaned_data['cpf'],
                username=form.cleaned_data['email'] 
            )
            
            # Faça login automaticamente após o registro
            login(request, user)
            
            # Redirecione para onde você deseja após o registro bem-sucedido
            return redirect('dashboard')  # Substitua 'dashboard' pela sua URL desejada
    else:
        form = RegisterForm()

    return render(request, 'author/pages/register.html', {'form': form})
        
        
        
        
        
def login_view(request):    
    form = LoginForm()
    return render(request, 'author/pages/login.html', {
        'form': form,
        'form_action': reverse('authors:login_create')
    })

# Importe a função split do Python para dividir o nome completo em partes
from django.contrib.auth import authenticate, login

def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)
    login_url = reverse('authors:login')

    if form.is_valid():
        cpf = form.cleaned_data.get('cpf', '')
        password = form.cleaned_data.get('password', '')
        authenticated_user = authenticate(request, cpf=cpf, password=password)

        if authenticated_user is not None:
            login(request, authenticated_user)
            
            # Obtenha o nome completo do usuário
            full_name = authenticated_user.get_full_name()
            
            # Divida o nome completo em partes
            parts = full_name.split()
            
            # Verifique se há pelo menos uma parte no nome
            if parts:
                # Use a primeira parte como o primeiro nome
                first_name = parts[0]
                
                # Armazene o primeiro nome na sessão
                request.session['user_name'] = first_name
            else:
                # Se o nome completo estiver vazio, use "Usuário" como padrão
                request.session['user_name'] = 'Usuário'
            
            messages.success(request, 'Você está logado.')
            return redirect('dashboard')  # Redireciona para o dashboard após o login
        else:
            messages.error(request, 'Login inválido')
    else:
        messages.error(request, 'Usuário ou senha incorreta')

    return redirect(login_url)


# views.py



def logout_view(request):
    logout(request)
    # Redireciona para a página de login ou para a home após o logout
    return redirect('home')
