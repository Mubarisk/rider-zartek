from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager


class Manager(UserManager):

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields["is_superuser"] = True
        super(Manager, self).create_superuser(
            username, email, password, **extra_fields
        )


class User(AbstractUser):
    class UserTypes(models.TextChoices):
        RIDER = "RIDER", "Rider"
        DRIVER = "DRIVER", "Driver"

    user_type = models.CharField(
        max_length=20, choices=UserTypes.choices, default=UserTypes.RIDER
    )

    def __str__(self):
        return self.username

    objects = Manager()
