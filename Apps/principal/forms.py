from django import forms 
from .models import * # Traer las tablas del modelo de base de datos en el archivo models.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model# importacion del modelo usuario personalizado para ser utilizado en vez del que viene por defecto
User = get_user_model()# Usar el modelo de Usuario personalizdo 



# formulario para  subir bicicletas 
class BicicletasForm(forms.ModelForm):
    class Meta:
        model = MiBicicleta # modelo usado para generar el formulario
        fields = ('marca','color','material','categoria','precioalquiler','foto') # campos que seran mostrados en la vista
        # fields = '__all__'
        #fields = ('apellidos',) 

# Creacion del formulario para el registro de usuarios en Biken usando el modelo personalizado
# de usuario(User) 
class CustomUserCreationForm(UserCreationForm):
    first_name= forms.CharField(required = True,)
    last_name = forms.CharField(required = True,)
    email = forms.EmailField(required = True,)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','numcelular', 'email', 'password1', 'password2'] 
        help_texts= {k:'' for k in fields}   


    def save(self,commit = True):   
        user = super(CustomUserCreationForm, self).save(commit = False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']


        if commit:
            user.save()

        return user
