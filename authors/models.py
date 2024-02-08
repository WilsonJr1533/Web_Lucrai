

# Create your models here.
from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('O campo Email é obrigatório'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser deve ter is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser deve ter is_superuser=True'))

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(_('endereço de email'), unique=True)
    cpf = models.CharField(max_length=11, unique=True)
    full_name = models.CharField(_('nome completo'), max_length=255, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['cpf']

    objects = CustomUserManager()

    # Redefine groups and user_permissions with a new related_name
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_name="custom_user_set",  # Evita conflitos com o modelo User padrão
        related_query_name="custom_user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="custom_user_set",  # Evita conflitos com o modelo User padrão
        related_query_name="custom_user",
    )

    def save(self, *args, **kwargs):
        self.full_name = f"{self.first_name} {self.last_name}".strip()
        super(CustomUser, self).save(*args, **kwargs)
