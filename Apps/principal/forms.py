from django import forms
from django.core import validators
from django.db.models import fields
from django.forms.fields import EmailField
from .models import * # Traer las tablas del modelo de base de datos en el archivo models.py
from .validators import *





# formulario para  subir bicicletas 
class BicicletasForm(forms.ModelForm):
    marca = forms.CharField(validators=[validatorLetters])
    foto = forms.ImageField(help_text='La imagen tiene que tener un formato valido, (preferible:jpg,png))')
    

    class Meta:
        model = MiBicicleta # modelo usado para generar el formulario de uploadbike
        fields = ('marca','color','material','categoria','precioalquiler','valortiempohoras','valortiempomin','descripcionbici','foto') # campos que seran mostrados en la vista
        # fields = '__all__'
        #fields = ('apellidos',) 


# formulario para editar bicicletas
class EditBicicletaForm(forms.ModelForm):
    marca = forms.CharField(validators=[validatorLetters])
    disponible = forms.BooleanField(required=False)
    foto = forms.ImageField(help_text='La imagen tiene que tener un formato valido, (preferible:jpg,png))')


    class Meta:
        model = MiBicicleta # modelo usado para generar el formulario de uploadbike
        fields = ('marca','color','material','categoria','precioalquiler','disponible','valortiempohoras','valortiempomin','descripcionbici','foto') # campos que seran mostrados en la vista
        # fields = '__all__'
        #fields = ('apellidos',) 


# formulario de contratos en bicicletas
class ContratoBicicletaForm(forms.ModelForm):
    numerodocumento = forms.CharField(validators=[validatornumdocumento])
    direccion = forms.CharField(validators=[validatordireccion])

    class Meta:
        model=  ContratoBicicleta # modelo usado para mostrar el formulario de contrato
        fields = ('tipodocumento','numerodocumento','direccion','horainicio','horafin')



# formulario de contacto de usuarios
class ContactoForm(forms.ModelForm):
    asunto = forms.CharField(validators=[validatorasunto])
    name = forms.CharField(validators=[validatorname])
    

    class Meta:
        model=Contacto
        fields =('name','email','tipo','asunto','mensaje')






