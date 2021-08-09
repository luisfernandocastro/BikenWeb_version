from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from .models import ContratoBicicleta, MiBicicleta, Perfil,CatalogoBicicleta
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



# @receiver(post_save,sender=ContratoBicicleta)
# def change_disponible(sender,instance,created, **kwargs):
#     if created:
#         MiBicicleta.objects.create(disponible=.)Z

@receiver(post_save, sender=ContratoBicicleta)
def change_disponible(sender, instance, **kwargs):
    instance.bicicleta.disponible = False # Puedes ser True o False
    instance.bicicleta.save()

