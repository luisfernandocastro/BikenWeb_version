from BikenPro.settings import MEDIA_URL, STATIC_URL
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.conf import settings
# User = get_user_model()

# Create your models here.

class User(AbstractUser):
    image_user = models.ImageField(upload_to='user/%Y/%m/%d',null=True,blank=True,verbose_name='Imagen de perfil')

    def get_image(self):
        if self.image_user:
            return '{}{}'.format(MEDIA_URL,self.image_user)
        return '{}{}'.format(STATIC_URL,'img/imgs_plus/user.png')


