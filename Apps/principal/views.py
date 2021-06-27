from django.urls import reverse_lazy # redireccion de funciones 
from django.shortcuts import get_object_or_404, redirect, render
from .models import * # se traen todas las tablas del modelo de base de datos
from .forms import  BicicletasForm,CustomUserCreationForm # importaciones del archivo forms.py
from django.contrib import messages # se muestran los mensajes apartir de una accion de un formulario...etc 
from django.contrib.auth import  authenticate,login as auth_login # Elementos necesarios para mostrar la vista de login generada por Django
from django.contrib.auth import get_user_model # importacion del modelo usuario personalizado para ser utilizado en vez del que viene por defecto
from django.contrib.auth.decorators import login_required # decorador para solicitar el login de un usuario para ver una vista no permitida sin loguearse
from django.utils.decorators import method_decorator 
from django.views.generic.edit import UpdateView # Actualiaciones  o ediciones de datos que se encuentran en la base de datos generadas por Django
user = get_user_model() # Usar el modelo de Usuario personalizdo 



# metodo para mostrar la vista del index del sitio web
def index(request):
    return render (request, 'index.html') 

# metodo para mostrar la vista de home y mostrar bicicletas en catalogo
def home(request):
    bicicletas = MiBicicleta.objects.all()# Se trae todos las bicicletas registradas en modelo de base de datod MIBicicleta 
    data = {
        'bicicletas' : bicicletas
    }
    return render (request, 'pages/inicio.html',data)

# metodo para mostrar el mensaje de registro exitoso al usuario
@login_required #Pedir al usuario iniciar sesion o registrarse para poder ver esta vista
def messageRegistro(request):
    return render (request, 'pages/completions_pages/correctRegistro.html')



# metodo para mostrar el mensaje de exitoso si la bicicleta se subio correctamente
@login_required #Pedir al usuario iniciar sesion o registrarse para poder ver esta vista
def messageUploadBike(request):
    return render (request, 'pages/completions_pages/correctUploadBike.html')


# metodo para mostrar la vista de Quienes somos (Biken) al usuario
def quienesSomos(request):
    return render (request, 'pages/quienessomos.html')

# metodo para mostrar la vista de contacto con Biken al usuario,
def contacto(request):
    return render (request, 'pages/Contacto.html')

# metodo para mostrar el formulario de registro al usuario
def registro(request):
    data={
        'form':CustomUserCreationForm()# Formulario personalizado  que se trae desde el forms.py
    }
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST,files=request.FILES)# request.FILES ,necesario para subir imagenes
        if formulario.is_valid():# validacion de los datos ingresados (si son correctos se procede a guardar estos datos)
            formulario.save()# Guardado de datos
            # Si  los datos ingresados son correctos el usuario queda logueado al momento
            user = authenticate(username=formulario.cleaned_data['username'],password=formulario.cleaned_data['password1'])
            auth_login(request,user)
            messages.success(request,"Te ha registrado correctamente")
            return redirect(to='messagereg') # redireccion de los datos validados correctamente a la ventana de exito
        data['form'] =  formulario


    return render (request, 'registration/registro.html',data) 


# metodo para el form de inicio Sesion,dado por Django
def login(request):
    return render (request, 'registration/login.html')


# metodo para la creacion de la vista del formulario de subir bicicleta por los usuarios que despues van hacer mostradas en 
# el catalo de ventana home(inicio)
@login_required # Pedir al usuario iniciar sesion o registrarse para poder subir una bicicleta 
def uploadBike(request):
    current_user = get_object_or_404(User, pk=request.user.pk)
    if request.method == 'POST':
        form = BicicletasForm(request.POST,files=request.FILES)# request.FILES ,necesario para subir imagenes
        if form.is_valid():
            bici = form.save(commit=False)
            bici.user = current_user
            bici.save()
            messages.success(request,"Inicia sesión para poder continúar")
            return redirect('messagebike')
    else:
        form = BicicletasForm()
    return render (request, 'pages/uploadBike.html',{'form': form})


# metodo para mostrar la vista de perfil del usuario logueado o de los demas usuarios registrados
@login_required # Pedir al usuario iniciar sesion o registrarse para poder ver los perfiles de los usuarios registrados
def profileUser(request, username=None):
    current_user = request.user
    if username and username != current_user.username:
        user = User.objects.get(username=username)
        miBici = user.miBici.all() # Se muestran las bicicletas subidas por los demas usuarios 
    else:
        miBici = current_user.miBici.all()# Se muestran las bicicletas subidas por el  usuario logueado
        user = current_user
    return render(request,'user/profile.html',{'user': user, 'miBici':miBici})



# metodo para editar o actualizar una bicicleta subida por el usuario loguedo
def editar_bicicleta(request,id):

    bicicleta = get_object_or_404(MiBicicleta,idmibicicleta=id)

    data = {
        'form': BicicletasForm(instance=bicicleta)
    }

    if request.method == 'POST':
        formulario = BicicletasForm(data=request.POST,instance=bicicleta, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect(to='perfil')
        data['form'] = BicicletasForm(instance=bicicleta.objects.get(idmibicicleta=id))

    return render(request,'bike/editar_bicicleta.html', data)


# metodo para actualizar o editar el perfil de un usuario registrado
@method_decorator(login_required, name='dispatch')# Pedir al usuario iniciar sesion o registrarse para poder editar su perfil
class ProfileUpdate(UpdateView):
    template_name = 'user/editprofile.html'
    model = Perfil # modelo utilizado para traer los datos a ser editados

    def get_object(self):
        profile, created = Perfil.objects.get_or_create(user=self.request.user)
        return profile

    fields = ['image_user','image_portada'] # campos a mostrar del formulario de edicion de perfil
    success_url=reverse_lazy('perfil')


