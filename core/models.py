from django.contrib.auth.models import AbstractUser
from django.db import models


#Custome User Model
class User(AbstractUser):
    email = models.EmailField(unique=True)
