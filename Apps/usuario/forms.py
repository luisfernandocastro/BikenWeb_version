
from django.core import validators
from django.db.models import fields
from Apps.principal.models import Perfil
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.forms.widgets import TextInput, Widget# importacion del modelo usuario personalizado para ser utilizado en vez del que viene por defecto
User = get_user_model()# Usar el modelo de Usuario personalizsdo 





class LoginForm(AuthenticationForm):
    def __init__(self, *args,**kwargs):
        super (LoginForm,self).__init__(*args,**kwargs)
        self.fields['username']
        self.fields['password']


# Creacion del formulario para el registro de usuarios en Biken usando el modelo personalizado
# de usuario(User) 
validatorFirst_name = RegexValidator("/^[a-zA-ZÀ-ÿ\s]{1,40}$/","El nombre no puede contener números, ni caracteres especiales")
validatorLast_name = RegexValidator("/^[a-zA-ZÀ-ÿ\s]{1,40}$/","El Apellido no puede contener números, ni caracteres especiales")
validatornumcelular = RegexValidator("/^\d{7,10}$/","Inserte un número de celular válido")

class CustomUserCreationForm(UserCreationForm):
    first_name= forms.CharField(required = True,validators=[validatorFirst_name])
    last_name = forms.CharField(required = True,validators=[validatorLast_name])
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




class UpdateUserForm(forms.ModelForm):

    username = forms.CharField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    numcelular = forms.IntegerField(required=False)

    class Meta:
        model = User
        fields = ['username','first_name','last_name','numcelular']




class ChangeEmailForm(forms.ModelForm):

    email = forms.EmailField(required=True,max_length=250, help_text='Requerido como maximo 250 carácteres como máximo y debe ser un email válido.')


    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(u'El email ya esta registrado , pueba con otro.')
        return email


class EditProfileForm(forms.ModelForm):
    class Meta:
        model= Perfil
        fields = ['telefono', 'direccion','estado', 'image_user', 'image_portada']