
from django.core import validators
from django.core.exceptions import ValidationError
from django.db.models import fields
from django.forms.fields import CharField
from Apps.principal.models import Perfil
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator, validate_slug
from django.forms.widgets import NumberInput, TextInput, Widget# importacion del modelo usuario personalizado para ser utilizado en vez del que viene por defecto
User = get_user_model()# Usar el modelo de Usuario personalizsdo 





class LoginForm(AuthenticationForm):
    def __init__(self, *args,**kwargs):
        super (LoginForm,self).__init__(*args,**kwargs)
        self.fields['username']
        self.fields['password']



validatorletters = RegexValidator(r"^[a-zA-ZÀ-ÿ\s]{1,40}$","Agrega solo letras")
validatorFirst_name = RegexValidator(r"^[a-zA-ZÀ-ÿ\s]{1,40}$","El nombre no puede contener números, ni caracteres especiales")
validatorLast_name = RegexValidator(r"^[a-zA-ZÀ-ÿ\s]{1,40}$","El Apellido no puede contener números, ni caracteres especiales")
validatornumcelular = RegexValidator("/^\d{7,10}$/","Inserte un número de celular válido")

# Creacion del formulario para el registro de usuarios en Biken usando el modelo personalizado
# de usuario(User) 
class CustomUserCreationForm(UserCreationForm):
    first_name= forms.CharField(required = True,validators=[validatorFirst_name])    
    last_name = forms.CharField(required = True,validators=[validatorLast_name])
    email = forms.EmailField(required = True)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','numcelular', 'email', 'password1', 'password2'] 
        help_texts= {k:'' for k in fields}   



    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(u'El email ya esta registrado , pueba con otro.')
        return email
    


    def clean_username(self):
        username = self.cleaned_data.get('username')
    
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(u'El nombre de usuario ya esta registrado en Biken')

        return username



    def clean_numcelular(self):
        numcelular = self.cleaned_data.get('numcelular')
    
    
        if not numcelular.isdigit():
            raise forms.ValidationError(u'El numero de celular solo puede contener numeros')

        return numcelular



class UpdateUserForm(forms.ModelForm):

    username = forms.CharField(required=True)
    first_name = forms.CharField(required=False,validators=[validatorFirst_name])
    last_name = forms.CharField(required=False,validators=[validatorLast_name])
    numcelular = forms.IntegerField(required=False)

    class Meta:
        model = User
        fields = ['username','first_name','last_name','numcelular']




    def clean_username(self):
        username = self.cleaned_data.get('username')
    
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(u'El nombre de usuario ya esta registrado en Biken')

        return username



    def clean_numcelular(self):
        numcelular = self.cleaned_data.get('numcelular')
    
        if not numcelular.isdigit():
            raise forms.ValidationError(u'El numero de celular solo puede contener numeros')

        return numcelular



class ChangeEmailForm(forms.ModelForm):
    estado = forms.CharField(validators=[validatorletters])

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


    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
    
        if not telefono.isdigit():
            raise forms.ValidationError(u'El telefono solo puede contener números')
    
        return telefono
    
