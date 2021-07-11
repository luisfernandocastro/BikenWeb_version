
# Elementos necesarios para mostrar la vista de login generada por Django
from django import forms

from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, logout,login as auth_login
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy  # redireccion de funciones
from django.shortcuts import redirect, render
from Apps.principal.models import Perfil  # se traen todas las tablas del modelo de base de datos
# importaciones del archivo forms.py
from .forms import CustomUserCreationForm,UpdateUserForm,ChangeEmailForm
# se muestran los mensajes apartir de una accion de un formulario...etc
from django.contrib import messages
# Elementos necesarios para mostrar la vista de login generada por Django
from django.contrib.auth.forms import  PasswordChangeForm

# importacion del modelo usuario personalizado para ser utilizado en vez del que viene por defecto
from django.contrib.auth import get_user_model,update_session_auth_hash
# decorador para solicitar el login de un usuario para ver una vista no permitida sin loguearse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Actualiaciones  o ediciones de datos que se encuentran en la base de datos generadas por Django
from django.views.generic.edit import UpdateView

from django.shortcuts import render

from django.conf import settings as setting
from django.contrib.auth.views import LoginView



User = get_user_model()



# -----------------------------------------login----------------------------------------------

#creacion de la clase de login con el loginview 

class Login(LoginView):
    template_name = 'registration/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated: # evita que el usuario logueado ingrese a la vista login  
            return redirect(setting.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar sesión'
        return context




class Logout(RedirectView):
    pattern_name = 'home'

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)


# def logoutUser(request):
#     logout(request)
#     return HttpResponseRedirect('/home')


def registro(request):
    data = {
        # Formulario personalizado  que se trae desde el forms.py
        'form': CustomUserCreationForm()
    }
    if request.user.is_authenticated:
        return redirect(setting.LOGIN_REDIRECT_URL)

    if request.method == 'POST':
        # request.FILES ,necesario para subir imagenes
        formulario = CustomUserCreationForm(
            data=request.POST, files=request.FILES)
        if formulario.is_valid():  # validacion de los datos ingresados (si son correctos se procede a guardar estos datos)
            formulario.save()  # Guardado de datos
            # Si  los datos ingresados son correctos el usuario queda logueado al momento
            user = authenticate(
                email=formulario.cleaned_data['email'], password=formulario.cleaned_data['password1'])
            auth_login(request, user)
            messages.success(request, "Te has registrado correctamente")
            # redireccion de los datos validados correctamente a la ventana de exito
            return redirect(to='messagereg')
        data['form'] = formulario

    return render(request, 'registration/registro.html', data)




    # metodo para mostrar la vista de perfil del usuario logueado o de los demas usuarios registrados
@login_required  # Pedir al usuario iniciar sesion o registrarse para poder ver los perfiles de los usuarios registrados
def profileUser(request, username=None):
    current_user = request.user
    if username and username != current_user.username:
        user = User.objects.get(username=username)
        miBici = user.miBici.all()  # Se muestran las bicicletas subidas por los demas usuarios
    else:
        # Se muestran las bicicletas subidas por el  usuario logueado
        miBici = current_user.miBici.all()
        user = current_user
    return render(request, 'user/profile.html', {'user': user, 'miBici': miBici})



@method_decorator(login_required, name='dispatch')
class UserUpdate(UpdateView):
    template_name = 'user/update_user.html'
    form_class = UpdateUserForm
    success_url = reverse_lazy('settings')

    def get_object(self):
        return self.request.user



# metodo para mostrar la vista de perfil del usuario logueado o de los demas usuarios registrados
@login_required  # Pedir al usuario iniciar sesion o registrarse para poder ver los perfiles de los usuarios registrados
def profileUser(request, username=None):
    current_user = request.user
    if username and username != current_user.username:
        user = User.objects.get(username=username)
        miBici = user.miBici.all()  # Se muestran las bicicletas subidas por los demas usuarios
    else:
        # Se muestran las bicicletas subidas por el  usuario logueado
        miBici = current_user.miBici.all()
        user = current_user
    return render(request, 'user/profile.html', {'user': user, 'miBici': miBici})



# metodo para actualizar o editar el perfil de un usuario registrado
# Pedir al usuario iniciar sesion o registrarse para poder editar su perfil
@method_decorator(login_required, name='dispatch')
class ProfileUpdate(UpdateView):
    template_name = 'user/editprofile.html'
    model = Perfil  # modelo utilizado para traer los datos a ser editados

    def get_object(self):
        profile, created = Perfil.objects.get_or_create(user=self.request.user)
        return profile

    # campos a mostrar del formulario de edicion de perfil
    fields = ['telefono', 'direccion',
        'biografia', 'image_user', 'image_portada']
    success_url = reverse_lazy('settings')





@method_decorator(login_required, name='dispatch')
class EmailUpdate(UpdateView):
    template_name = 'user/edit_email.html'
    form_class = ChangeEmailForm
    success_url = reverse_lazy('settings')

    def get_object(self):
        return self.request.user

    def get_form(self, form_class=None):
        form = super(EmailUpdate, self).get_form()
        form.fields['email'].widget = forms.EmailInput(
            attrs={'class': 'form-control-file mt-3', 'placeholder': 'Email'})
        return form



@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)
            messages.success(request,'Tu contraseña a sido cambiada correctamente!!')
            return redirect('settings')
        else:
            messages.error(request,'Por favor corrija los errores')
    else:
        form = PasswordChangeForm(request.user)
    return render(request,'user/change_password.html',{'form':form})





    # # metodo para el form de inicio Sesion,dado por Django
# def login(request):
#     return render(request, 'registration/login.html')

# class Login(FormView):
#     template_name = 'registration/login.html'
#     form_class = AuthenticationForm
#     success_url = reverse_lazy('home')


#     @method_decorator(csrf_protect)
#     @method_decorator(never_cache)
#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return HttpResponseRedirect(self.get_success_url())
#         else:
#             return super(Login,self).dispatch(request, *args, **kwargs)
    
#     def form_valid(self,form):
#         auth_login(self.request,form.get_user())
#         return super(Login,self).form_valid(form)

# def logoutUser(request):
#     logout(request)
#     return HttpResponseRedirect('/home')


# class Login(FormView):
#     template_name = 'registration/login.html'
#     form_class = AuthenticationForm
#     success_url = reverse_lazy('home')

#     def dispatch(self,request,*args,**kwargs):
#         if request.user.is_authenticated:
#             return HttpResponseRedirect(self.success_url)
#         else:
#             return super(Login,self).dispatch(request, *args, **kwargs)
    
#     def form_valid(self,form):
#         auth_login(self.request,form.get_user())
#         return HttpResponseRedirect(self.success_url)
