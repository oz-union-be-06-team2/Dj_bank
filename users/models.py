from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(max_length=45, unique=True, null=False)
    nickname = models.CharField(max_length=15, unique=True, null=False)
    phone_num = models.CharField(max_length=15, unique=True, null=False)
