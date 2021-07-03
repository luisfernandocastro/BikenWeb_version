from django import forms
from .models import * # Traer las tablas del modelo de base de datos en el archivo models.py




# formulario para  subir bicicletas 
class BicicletasForm(forms.ModelForm):
    foto = forms.ImageField(help_text='La imagen tiene que tener un formato valido, (preferible:jpg,png))')


    class Meta:
        model = MiBicicleta # modelo usado para generar el formulario
        fields = ('marca','color','material','categoria','precioalquiler','valortiempohoras','valortiempomin','descripcionbici','foto') # campos que seran mostrados en la vista
        # fields = '__all__'
        #fields = ('apellidos',) 




#







