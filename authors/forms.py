import re
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm




def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()
    
def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)
   
def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError((
            'Senha muito fraca'
        ),
            code='invalid'
        )


    
class RegisterForm(forms.Form):
    nome_completo = forms.CharField(
        max_length=100, 
        label='Nome completo', 
        widget=forms.TextInput(attrs={'placeholder': 'Escreva seu nome'})
    )
    cpf = forms.CharField(
        max_length=14, 
        label='CPF', 
        widget=forms.TextInput(attrs={'placeholder': 'Escreva seu CPF'})
        # Adicione aqui qualquer validador específico para CPF se necessário
    )
    data_nascimento = forms.DateField(
        label='Data de nascimento', 
        widget=forms.DateInput(attrs={'placeholder': 'Data de nascimento', 'type': 'date'})
    )
    email = forms.EmailField(
        label='Email', 
        widget=forms.EmailInput(attrs={'placeholder': 'Seu melhor email'})
    )
    password = forms.CharField(
        label='Senha', 
        widget=forms.PasswordInput(attrs={'placeholder': 'Escreva sua senha'}),
        help_text='A senha deve ter pelo menos uma letra maiúscula, uma letra minúscula e um número. O comprimento deve ser pelo menos 8 caracteres.',
        validators=[validate_password, strong_password],
    )
    password2 = forms.CharField(
        label='Confirme sua senha', 
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirme sua senha'})
    )
    
   
    
    
    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'As senhas precisam ser iguais',
                code='invalid'
            )
            raise ValidationError({
                
                'password2': [
                    password_confirmation_error,
                ],
            }) 
 # Importe o modelo de usuário personalizado

class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['cpf'], 'Digite seu CPF')
        add_placeholder(self.fields['password'], 'Digite sua senha')
    
    cpf = forms.CharField(
        error_messages={'required': 'Digite seu CPF'},
        label='CPF')
    password = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Por favor, digite sua senha'
        },
        label='Senha'
    )
