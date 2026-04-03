from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('Имейлът е задължителен'))

        if not password:
            raise ValueError(_('Паролата е задължителна'))

        email = self.normalize_email(email)
        extra_fields.setdefault('role', CustomUser.RoleChoices.TRAVELER)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', CustomUser.RoleChoices.ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None

    class RoleChoices(models.TextChoices):
        TRAVELER = 'TRAVELER', _('Пътуващ')
        OPERATOR = 'OPERATOR', _('Оператор')
        ADMIN = 'ADMIN', _('Администратор')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    email = models.EmailField(
        unique=True,
        blank=False,
        verbose_name=_('Имейл'),
        error_messages={
            'unique': _('Потребител с този имейл вече съществува.')
        }
    )

    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True,
        verbose_name=_('Профилна снимка')
    )

    bio = models.TextField(
        blank=True,
        verbose_name=_('Описание'),
        help_text=_('Кратка информация за потребителя')
    )

    role = models.CharField(
        max_length=20,
        choices=RoleChoices.choices,
        default=RoleChoices.TRAVELER,
        verbose_name=_('Роля'),
        help_text=_('Определя правата на потребителя'),
    )

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.email = self.__class__.objects.normalize_email(self.email)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Потребител')
        verbose_name_plural = _('Потребители')


    @property
    def is_traveler(self):
        return self.role == self.RoleChoices.TRAVELER

    @property
    def is_operator(self):
        return self.role == self.RoleChoices.OPERATOR

    @property
    def is_admin(self):
        return self.role == self.RoleChoices.ADMIN or self.is_superuser

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.email

