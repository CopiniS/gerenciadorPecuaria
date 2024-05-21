from django.db import models
from django.contrib.auth.models import AbstractUser

class Produtor(AbstractUser):
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=16)
    email = models.CharField(max_length=255, unique = True)
    password = models.CharField(max_length=255)
    telefone1 = models.CharField(max_length=15)
    telefone2 = models.CharField(max_length=15, null=True)

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []