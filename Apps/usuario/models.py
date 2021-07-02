from re import VERBOSE
from BikenPro.settings import MEDIA_URL, STATIC_URL
from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.conf import settings
# User = get_user_model()

# Create your models here.

class User(AbstractUser):
    email = models.EmailField('correo Electronico',unique=True)
    numcelular = models.CharField(db_column='numero Celular',null=True,verbose_name='Celular', max_length=10, validators=[MinLengthValidator(10)])


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
