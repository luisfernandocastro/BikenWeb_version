from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from .models import ContratoBicicleta, MiBicicleta, Perfil,CatalogoBicicleta
from django.dispatch import receiver


User=get_user_model()

# Crea automaticamente un perfil del usuario registrado
@receiver(post_save,sender=User)
def create_profile(sender,instance,created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)


# Cambia la disponibilidad ( True= False) de la bicicleta al completar el contrato de esta bicicleta
@receiver(post_save, sender=ContratoBicicleta)
def change_disponible(sender, instance, **kwargs):
    instance.bicicleta.disponible = False # Puedes ser True o False
    instance.bicicleta.save() 

