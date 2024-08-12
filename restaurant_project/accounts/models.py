from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.managers import CustomUserManager


# Create your models here.
class UserModel(AbstractUser):
    ROLES_CHOICES=[
        ('reception','RECEPTION'),
        ('waiter','WAITER'),
    ]
    email= models.EmailField(unique=True)
    roles = models.CharField(choices=ROLES_CHOICES,max_length=50)

    USERNAME_FIELD="email"
    REQUIRED_FIELDS=[]


    objects = CustomUserManager()