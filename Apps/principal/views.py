from django import forms
from django.urls import reverse_lazy  # redireccion de funciones
from django.shortcuts import get_object_or_404, redirect, render
from .models import *  # se traen todas las tablas del modelo de base de datos
# importaciones del archivo forms.py
from .forms import BicicletasForm, CustomUserCreationForm,ChangeEmailForm,UpdateUserForm
# se muestran los mensajes apartir de una accion de un formulario...etc
from django.contrib import messages
# Elementos necesarios para mostrar la vista de login generada por Django
from django.contrib.auth import authenticate, login as auth_login
# importacion del modelo usuario personalizado para ser utilizado en vez del que viene por defecto
from django.contrib.auth import get_user_model
# decorador para solicitar el login de un usuario para ver una vista no permitida sin loguearse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Actualiaciones  o ediciones de datos que se encuentran en la base de datos generadas por Django
from django.views.generic.edit import UpdateView
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
user = get_user_model()  # Usar el modelo de Usuario personalizdo


# metodo para mostrar la vista del index del sitio web
def index(request):
    return render(request, 'index.html')


# metodo para mostrar el mensaje de registro exitoso al usuario
@login_required  # Pedir al usuario iniciar sesion o registrarse para poder ver esta vista
def messageRegistro(request):
    return render(request, 'pages/completions_pages/correctRegistro.html')


# metodo para mostrar el mensaje de exitoso si la bicicleta se subio correctamente
@login_required  # Pedir al usuario iniciar sesion o registrarse para poder ver esta vista
def messageUploadBike(request):
    return render(request, 'pages/completions_pages/correctUploadBike.html')


# metodo para mostrar la vista de Quienes somos (Biken) al usuario
def quienesSomos(request):
    return render(request, 'pages/quienessomos.html')

# metodo para mostrar la vista de contacto con Biken al usuario,


def contacto(request):
    return render(request, 'pages/Contacto.html')

# metodo para mostrar el formulario de registro al usuario


def registro(request):
    data = {
        # Formulario personalizado  que se trae desde el forms.py
        'form': CustomUserCreationForm()
    }
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
            messages.success(request, "Te ha registrado correctamente")
            # redireccion de los datos validados correctamente a la ventana de exito
            return redirect(to='messagereg')
        data['form'] = formulario

    return render(request, 'registration/registro.html', data)


# metodo para el form de inicio Sesion,dado por Django
def login(request):
    return render(request, 'registration/login.html')


# metodo para la creacion de la vista del formulario de subir bicicleta por los usuarios que despues van hacer mostradas en
# el catalo de ventana home(inicio)
# Pedir al usuario iniciar sesion o registrarse para poder subir una bicicleta
@login_required
def uploadBike(request):
    current_user = get_object_or_404(User, pk=request.user.pk)
    if request.method == 'POST':
        # request.FILES ,necesario para subir imagenes
        form = BicicletasForm(request.POST, files=request.FILES)
        if form.is_valid():
            bici = form.save(commit=False)
            bici.user = current_user
            bici.save()
            messages.success(request, "Inicia sesión para poder continúar")
            return redirect('messagebike')
    else:
        form = BicicletasForm()
    return render(request, 'bike/uploadBike.html', {'form': form})


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


# metodo para editar o actualizar una bicicleta subida por el usuario loguedo
def editar_bicicleta(request, id):

    bicicleta = get_object_or_404(MiBicicleta, idmibicicleta=id)

    data = {
        'form': BicicletasForm(instance=bicicleta)
    }

    if request.method == 'POST':
        formulario = BicicletasForm(
            data=request.POST, instance=bicicleta, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect(to='perfil')
        data['form'] = BicicletasForm(
            instance=bicicleta.objects.get(idmibicicleta=id))

    return render(request, 'bike/editar_bicicleta.html', data)


def delete_bicicleta(request, id):
    bicicleta = get_object_or_404(MiBicicleta, idmibicicleta=id)
    bicicleta.delete()
    return redirect(to="perfil")


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
    fields = ['telefono','direccion','biografia','image_user', 'image_portada']
    success_url = reverse_lazy('perfil')



# metodo para mostrar la vista de home y mostrar bicicletas en catalogo
def home(request):

    # Se trae todos las bicicletas registradas en modelo de base de datod MIBicicleta
    bicicletas = MiBicicleta.objects.all()
    # Valor 1: Número de todos los datos actuales
    # Valor 2: cuántos datos se muestran por página
    # Valor 3: cuando la última página tiene menos de n datos, combine los datos en la página anterior
    paginator = Paginator(bicicletas, 12, 3)
    try:
        # GET request method get () Obtiene el valor correspondiente al valor clave especificado
        num = request.GET.get('list', '1')
        number = paginator.page(num)

    except PageNotAnInteger:
        # Si el número de números de página ingresados ​​por url no es un número entero, muestre la primera página de datos
        # ejemplo http://localhost:8000/home/?page=n  (n no es numero, por lo tanto se redirecciona a la primera pagina)
        number = paginator.page(1)

    except EmptyPage:
        # Si el número de página no está en el rango de números de página actual, se muestra la última página
        # paginator.num_pages Obtenga el número total actual de páginas
        # paginator.page () Obtener una página especificada
        number = paginator.page(paginator.num_pages)

        # number representa el contenido de una página, el paginator representa el contenido de todas las páginas
    return render(request, 'pages/inicio.html', {'page': number, 'paginator': paginator})



@method_decorator(login_required,name='dispatch')
class EmailUpdate(UpdateView):
    template_name='user/edit_email.html'
    form_class= ChangeEmailForm
    success_url = reverse_lazy('perfil')

    def get_object(self):
        return self.request.user

    def get_form(self, form_class=None):
        form = super(EmailUpdate,self).get_form()
        form.fields['email'].widget = forms.EmailInput(attrs={'class':'form-control-file mt-3','placeholder':'Email'})
        return form




@method_decorator(login_required,name='dispatch')
class UserUpdate(UpdateView):
    template_name='user/update_user.html'
    form_class= UpdateUserForm
    success_url = reverse_lazy('perfil')

    def get_object(self):
        return self.request.user

    # def get_form(self, form_class=None):
    #     form = super(EmailUpdate,self).get_form()
    #     form.fields['email'].widget = forms.EmailInput(attrs={'class':'form-control-file mt-3','placeholder':'Email'})
    #     return form