import django
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from .forms import PersonaForm, BicicletasForm,CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate,login as auth_login
from Apps.usuario.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
user = get_user_model()
# Create your views here.


def index(request):
    return render (request, 'index.html') 


def home(request):
    bicicletas = MiBicicleta.objects.all()
    data = {
        'bicicletas' : bicicletas
    }
    return render (request, 'pages/inicio.html',data)


def messageRegistro(request):
    return render (request, 'pages/completions_pages/correctRegistro.html')

@login_required
def messageUploadBike(request):
    return render (request, 'pages/completions_pages/correctUploadBike.html')


def quienesSomos(request):
    return render (request, 'pages/quienessomos.html')


def contacto(request):
    return render (request, 'pages/Contacto.html')


def registro(request):
    data={
        'form':CustomUserCreationForm()
    }
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST,files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data['username'],password=formulario.cleaned_data['password1'])
            auth_login(request,user)
            messages.success(request,"Te ha registrado correctamente")
            return redirect(to='messagereg')
        data['form'] =  formulario
    return render (request, 'registration/registro.html',data) 
    # contexto={
    #         'form':form
    #     }
    # else: 
    #     form = PersonaForm(request.POST)
    #     contexto={
    #         'Form':form
    #     



def login(request):
    return render (request, 'registration/login.html')


def murouser(request):
    return render (request, 'pages/muroUser.html')


@login_required
def uploadBike(request):
    current_user = get_object_or_404(User, pk=request.user.pk)
    if request.method == 'POST':
        form = BicicletasForm(request.POST,files=request.FILES)
        if form.is_valid():
            bici = form.save(commit=False)
            bici.user = current_user
            bici.save()
            messages.success(request,"Inicia sesión para poder continúar")
            return redirect('messagebike')
    else:
        form = BicicletasForm()
    return render (request, 'pages/uploadBike.html',{'form': form})


    # if request.method == 'GET':
    #     form = BicicletasForm()
    #     contexto={
    #         'FormBike':form
    #     }
    # else: 
    #     form = BicicletasForm(request.POST,files=request.FILES)
    #     contexto={
    #         'FormBike':form
    #     }
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request,"Inicia sesión para poder continúar")
    #         return redirect('messagebike')

    # return render (request, 'pages/uploadBike.html',contexto)
@login_required
def profileUser(request, username=None):
    current_user = request.user
    if username and username != current_user.username:
        user = User.objects.get(username=username)
        miBici = user.miBici.all()
    else:
        miBici = current_user.miBici.all()
        user = current_user
    return render(request,'user/profile.html',{'user': user, 'miBici':miBici})