from django.contrib.auth.models import AbstractUser
from django.db import models

from user.managers import UserManager


class User(AbstractUser):
    cpf = models.CharField(max_length=14, unique=True)
    password = models.CharField(
        max_length=50, blank=False, null=False, verbose_name="Senha"
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    username = None

    objects = UserManager()

    USERNAME_FIELD: str = 'cpf'
    REQUIRED_FIELDS: list[str] = ["first_name", "last_name", "email"]

    def __str__(self) -> str:
        return self.email
