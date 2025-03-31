from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        USER = "USER", "User"

    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.USER)

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username
