from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    # creating our own user auth, use this class instead of user class in the authentication
    email = models.EmailField(unique=True)