from django import forms
from django.forms.widgets import TextInput
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = '__all__'
        #fields = ('apellidos',) 


class BicicletasForm(forms.ModelForm):
    class Meta:
        model = MiBicicleta
        fields = ('marca','color','material','categoria','precioalquiler','foto')
        # fields = '__all__'
        #fields = ('apellidos',) 


class CustomUserCreationForm(UserCreationForm):
    first_name= forms.CharField(required = True,)
    last_name = forms.CharField(required = True,)
    email = forms.EmailField(required = True,)
    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'email', 'password1', 'password2'] 
        help_texts= {k:'' for k in fields}   



    def save(self,commit = True):   
        user = super(CustomUserCreationForm, self).save(commit = False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']


        if commit:
            user.save()

        return user
