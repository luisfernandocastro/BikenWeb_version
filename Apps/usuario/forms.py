
from django.core.exceptions import ValidationError
from django.db.models import fields
from django.forms.fields import CharField
from Apps.principal.models import Perfil
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator, validate_slug
from django.forms.widgets import NumberInput, TextInput, Widget# importacion del modelo usuario personalizado para ser utilizado en vez del que viene por defecto
from Apps.principal.validators import *
User = get_user_model()# Usar el modelo de Usuario personalizsdo 




# Formulario de Login basado en la clase de AuthenticationForm
class LoginForm(AuthenticationForm):
    def __init__(self, *args,**kwargs): # Metodo inicializador
        super (LoginForm,self).__init__(*args,**kwargs) # herencia de la clase padre
        self.fields['username'] # se sobreescribe la variable [username] 
        self.fields['password'] # se sobreescribe la variable [password] 




# Creacion del formulario para el registro de usuarios en Biken usando el modelo personalizado
# de usuario(User) 
class CustomUserCreationForm(UserCreationForm):
    first_name= forms.CharField(required = True,validators=[validatorFirst_name])    
    last_name = forms.CharField(required = True,validators=[validatorLast_name])
    email = forms.EmailField(required = True)
    class Meta:
        model = User
        # campos a mostrar en el template
        fields = ['username','first_name','last_name','numcelular', 'email', 'password1', 'password2'] 
        help_texts= {k:'' for k in fields}   # No muestra los textos de ayuda que vienen po defecto en Django en el formulario de registro


    # validacion del email,evita que se guarde uno repetido en la base datos
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists(): # verifica que el email ingresado ya encuentre
            raise forms.ValidationError(u'El email ya esta registrado , pueba con otro.')
        return email
    

    # validacion de nombre de usuario,muestra error si el nombre de usuario ya se encuentra en la base de datos
    def clean_username(self):
        username = self.cleaned_data.get('username')
    
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(u'El nombre de usuario ya esta registrado en Biken')

        return username






# actualizacion de los datos secundarios de registro
class UpdateUserForm(forms.ModelForm):

    username = forms.CharField(required=False)
    first_name = forms.CharField(required=False,validators=[validatorFirst_name])
    last_name = forms.CharField(required=False,validators=[validatorLast_name])
    numcelular = forms.IntegerField(required=False,validators=[validatornumcelular])

    class Meta:
        model = User
        # campos a mostrar en el template
        fields = ['username','first_name','last_name','numcelular']





# formulario de cambio de email
class ChangeEmailForm(forms.ModelForm):

    email = forms.EmailField(required=True,max_length=250, help_text='Requerido como maximo 250 carácteres como máximo y debe ser un email válido.')

    class Meta:
        model = User
        # campo a mostrar en el template
        fields = ['email']

    # validacion del email,evita que se guarde uno repetido en la base datos
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(u'El email ya esta registrado , pueba con otro.')
        return email

# formulario de edicion de perfil del usuario
class EditProfileForm(forms.ModelForm):
    estado = forms.CharField(required=False,validators=[validatorEstado])
    telefono = forms.CharField(validators=[validatornumtelefono])    
    direccion = forms.CharField(required=False, validators=[validatordireccion])

    class Meta:
        model= Perfil
        # campos a mostrar en el template
        fields = ['telefono', 'direccion','estado', 'image_user', 'image_portada']



