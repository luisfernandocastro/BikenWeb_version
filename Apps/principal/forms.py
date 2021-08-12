from django import forms
from django.core import validators
from django.core.validators import RegexValidator
from django.db.models import fields
from .models import * # Traer las tablas del modelo de base de datos en el archivo models.py


# validators
validatorLetters= RegexValidator(r"^[a-zA-ZÀ-ÿ\s]{1,40}$","El campo de marca solo puede contener letras")
validatornum= RegexValidator(r"^[a-zA-ZÀ-ÿ\s]{1,40}$","El campo de marca solo puede contener letras")


# formulario para  subir bicicletas 
class BicicletasForm(forms.ModelForm):
    marca = forms.CharField(validators=[validatorLetters])
    foto = forms.ImageField(help_text='La imagen tiene que tener un formato valido, (preferible:jpg,png))')

    class Meta:
        model = MiBicicleta # modelo usado para generar el formulario de uploadbike
        fields = ('marca','color','material','categoria','precioalquiler','valortiempohoras','valortiempomin','descripcionbici','foto') # campos que seran mostrados en la vista
        # fields = '__all__'
        #fields = ('apellidos',) 



class EditBicicletaForm(forms.ModelForm):
    marca = forms.CharField(validators=[validatorLetters])
    disponible = forms.BooleanField(required=False)
    foto = forms.ImageField(help_text='La imagen tiene que tener un formato valido, (preferible:jpg,png))')


    class Meta:
        model = MiBicicleta # modelo usado para generar el formulario de uploadbike
        fields = ('marca','color','material','categoria','precioalquiler','disponible','valortiempohoras','valortiempomin','descripcionbici','foto') # campos que seran mostrados en la vista
        # fields = '__all__'
        #fields = ('apellidos',) 



class ContratoBicicletaForm(forms.ModelForm):
    class Meta:
        model=  ContratoBicicleta
        fields = ('tipodocumento','numerodocumento','direccion','horainicio','horafin')









