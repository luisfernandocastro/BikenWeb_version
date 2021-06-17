from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from .models import Perfil
from django.dispatch import receiver


User=get_user_model()

@receiver(post_save,sender=User)
def create_profile(sender,instance,created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)
