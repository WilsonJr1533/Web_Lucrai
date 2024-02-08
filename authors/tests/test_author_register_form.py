from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized
from authors.forms import RegisterForm




class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Seu usuário'),
        ('email', 'Seu email'),
        ('first_name', 'Ex.: João'),
        ('last_name', 'Ex.: Silva'),
        ('password', 'Escreva sua senha'),
        ('password2', 'Confirme sua senha'),
    ])
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, placeholder)
        
    @parameterized.expand([
        ('username', (
            'Obrigatório. 150 caracteres ou menos. '
            'Letras, números e @/./+/-/_ apenas.')),
        ('email', 'Email precisa ser válido.'),
        ('password', (
            'A senha deve ter pelo menos uma letra maiúscula, '
            'uma letra minúscula e um número. O comprimento deve ser '
            'pelo menos 8 caracteres.'
        )),
    ])
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, needed)
        
    @parameterized.expand([
        ('username', 'Nome de Usuário'),
        ('first_name', 'Primeiro nome'),
        ('last_name', 'Sobrenome'),
        ('email', 'E-mail'),
        ('password', 'Senha'),
        ('password2', 'Confirme sua senha'),
    ])
    def test_fields_label(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(current, needed)
        
        
class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@anyemail.com',
            'password': 'Str0ngP@ssword1',
            'password2': 'Str0ngP@ssword1',
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'Este campo não pode estar vazio.'),
        ('first_name', 'Escreva seu nome.'),
        ('last_name', 'Escreva seu sobrenome.'),
        ('password2', 'Por favor, Confirme sua senha.'),
        ('email', 'E-mail é obrigatório.'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))
        
        
    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'abc123'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = (
            'A senha deve ter pelo menos uma letra maiúscula, '
            'uma letra minúscula e um número. O comprimento deve ser '
            'pelo menos 8 caracteres.'
        )

        
        self.assertIn(msg, response.content.decode('utf-8'))

        self.form_data['password'] = '@A123abc123'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertNotIn(msg, response.context['form'].errors.get('password'))

    def test_password_and_password_confirmation_are_equal(self):
        self.form_data['password'] = '@A123abc123'
        self.form_data['password2'] = '@A123abc1235'

        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'As senhas precisam ser iguais'
        
        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))


    def test_email_field_must_be_unique(self):
        url = reverse('authors:register_create')

        self.client.post(url, data=self.form_data, follow=True)
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Esse email já está cadastrado'
        self.assertIn(msg, response.context['form'].errors.get('email'))
        self.assertIn(msg, response.content.decode('utf-8'))
        
        
        def test_author_created_can_login(self):
            url = reverse('authors:register_create')

            self.form_data.update({
                'username': 'testuser',
                'password': '@Bc123456',
                'password2': '@Bc123456',
            })

            self.client.post(url, data=self.form_data, follow=True)

            is_authenticated = self.client.login(
                username='testuser',
                password='@Bc123456'
            )

            self.assertTrue(is_authenticated)