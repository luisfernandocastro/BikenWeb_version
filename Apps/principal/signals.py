from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from .models import MiBicicleta, Perfil,CatalogoBicicleta
from django.dispatch import receiver


User=get_user_model()

@receiver(post_save,sender=User)
def create_profile(sender,instance,created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)


# @receiver(post_save,sender=MiBicicleta)
# def create_catalogoBicicleta(sender,instance,created,**kwargs):
#     if created:
#         CatalogoBicicleta.objects.create(bicicleta=instance)