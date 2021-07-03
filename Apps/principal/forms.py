from django import forms
from django.forms import fields, widgets
from django.forms.fields import EmailField 
from .models import * # Traer las tablas del modelo de base de datos en el archivo models.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model# importacion del modelo usuario personalizado para ser utilizado en vez del que viene por defecto
User = get_user_model()# Usar el modelo de Usuario personalizdo 



# formulario para  subir bicicletas 
class BicicletasForm(forms.ModelForm):
    foto = forms.ImageField(help_text='La imagen tiene que tener un formato valido, (preferible:jpg,png))')


    class Meta:
        model = MiBicicleta # modelo usado para generar el formulario
        fields = ('marca','color','material','categoria','precioalquiler','valortiempohoras','valortiempomin','descripcionbici','foto') # campos que seran mostrados en la vista
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

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(u'El email ya esta registrado , pueba con otro.')
        return email



#
class UpdateUserForm(forms.ModelForm):

    username = forms.CharField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    numcelular = forms.IntegerField(required=False)

    class Meta:
        model = User
        fields = ['username','first_name','last_name','numcelular']

    # def  clean_username(self):
    #     username=self.cleaned_data.get('username')
    #     if 'username' in self.changed_data:
    #         if User.objects.filter(username=username).exists():
    #             raise forms.validationError(u'El username ya esta registrado,prueba con otro.') 
    #     return username    



class ChangeEmailForm(forms.ModelForm):

    email = forms.EmailField(required=True,max_length=250, help_text='Requerido como maximo 250 carácteres como máximo y debe ser un email válido.')


    class Meta:
        model = User
        fields = ['email']

    # def  clean_email(self):
    #     email=self.cleaned_data.get('email')
    #     if 'email' in self.changed_data:
    #         if User.objects.filter(email=email).exists():
    #             raise forms.validationError(u'El email ya esta registrado,prueba con otro.') 
    #     return email


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(u'El email ya esta registrado , pueba con otro.')
        return email