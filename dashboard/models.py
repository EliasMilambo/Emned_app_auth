from django.db import models
from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):
    # first_name, last_name, email et username sont déjà inclus dans AbstractUser
    phone = models.CharField(max_length=20, blank=True, null=True)

    # On surcharge pour rendre l'email obligatoire à la création
    email = models.EmailField(unique=True)

    # Par défaut, le compte est désactivé jusqu'à validation du mail
    is_active = models.BooleanField(default=False)
