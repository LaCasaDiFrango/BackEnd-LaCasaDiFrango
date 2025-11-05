from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class PerfilChoices(models.TextChoices):
    USUARIO = 'usuario', 'Usuário'
    ADMIN = 'administrador', 'Administrador'


class UserManager(BaseUserManager):
    """Manager para usuários."""

    use_in_migrations = True

    def create_user(self, email, password=None, perfil=PerfilChoices.USUARIO, **extra_fields):
        """Cria, salva e retorna um novo usuário."""
        if not email:
            raise ValueError('O usuário deve ter um endereço de email.')

        extra_fields.setdefault('perfil', perfil)

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Cria, salva e retorna um superusuário."""
        user = self.create_user(email, password, perfil=PerfilChoices.ADMIN)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Modelo de usuário do sistema."""

    passage_id = models.CharField(
        max_length=255, null=True, blank=True,
        verbose_name=_('passage_id'),
        help_text=_('Passage ID')
    )
    email = models.EmailField(
        max_length=255, unique=True,
        verbose_name=_('email'),
        help_text=_('Email')
    )
    name = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name=_('name'),
        help_text=_('Nome do usuário')
    )
    endereco = models.ForeignKey(
        'Endereco',
        on_delete=models.PROTECT,
        null=True, blank=True,
        related_name='enderecos',
        verbose_name=_('endereço'),
        help_text=_('Endereço do usuário')
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    perfil = models.CharField(
        max_length=20,
        choices=PerfilChoices.choices,
        default=PerfilChoices.USUARIO,
        verbose_name=_('perfil'),
        help_text=_('Tipo de perfil do usuário')
    )

    # Novo campo para armazenar a data do último pedido
    ultimo_pedido = models.DateTimeField(
        null=True, blank=True,
        verbose_name=_('Último pedido'),
        help_text=_('Data do último pedido realizado pelo usuário')
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
