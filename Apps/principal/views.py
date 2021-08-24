from typing import Reversible
from django import forms
import django
from django.core.mail.message import EmailMultiAlternatives
from django.http.response import HttpResponse, HttpResponseRedirect
from django.template import context
from django.template.context import RequestContext
from django.views.generic import DeleteView ,TemplateView
from django.urls import reverse_lazy  # redireccion de funciones
from django.shortcuts import get_object_or_404, redirect, render # importacions a usar en las vistas basadas en funciones
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from .models import *  # se traen todas las tablas del modelo de base de datos
# importaciones del archivo forms.py
from .forms import BicicletasForm, ContactoForm,EditBicicletaForm,ContratoBicicletaForm
# se muestran los mensajes apartir de una accion de un formulario...etc
from django.contrib import messages
# importacion del modelo usuario personalizado para ser utilizado en vez del que viene por defecto
from django.contrib.auth import get_user_model
# decorador para solicitar el login de un usuario para ver una vista no permitida sin loguearse
from django.contrib.auth.decorators import login_required
# Actualiaciones  o ediciones de datos que se encuentran en la base de datos generadas por Django
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin # mensajes a mostrar en las vistas basadas en clases
from django.contrib.auth.mixins import LoginRequiredMixin # Mixin para solicitar el logueo de usuario para ver la vista( vistas basadas en clases)


from django.core.mail import EmailMessage, send_mail
# start importaciones pdf------------

import os
from django.http import HttpResponse
from django.conf.global_settings import STATIC_ROOT,STATIC_URL,MEDIA_ROOT,MEDIA_URL
from django.conf import settings as conf_settings
from django.template import Context
from django.template.loader import get_template, render_to_string 
from xhtml2pdf import pisa 

# end importaciones pdf------------

from hashlib import sha1

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
    if request.user.is_authenticated:
        numcontratos = ContratoBicicleta.objects.filter(bicicleta__user=request.user).count()
        nummensajes = Contacto.objects.all().count()
    return render(request, 'pages/quienessomos.html',{'numcontratos':numcontratos,'nummensajes':nummensajes})




# metodo para la creacion de la vista del formulario de subir bicicleta por los usuarios que despues van hacer mostradas en
# el catalo de ventana home(inicio)
# Pedir al usuario iniciar sesion o registrarse para poder subir una bicicleta
@login_required
def uploadBike(request):
    current_user = get_object_or_404(User, pk=request.user.pk)

    if request.user.is_authenticated:
        numcontratos = ContratoBicicleta.objects.filter(bicicleta__user=request.user).count()
        nummensajes = Contacto.objects.all().count()


    if request.method == 'POST':
        # request.FILES ,necesario para subir imagenes
        form = BicicletasForm(request.POST, files=request.FILES) # FILES sube la imagen seleccionada a la base de datos
        if form.is_valid(): # se valida si el formulario es correcto
            bici = form.save(commit=False) # necesario para traer datos de otras instancias
            bici.user = current_user # Le asigno al campo de usuario(user) la pk del usuario logueado 
            bici.save() # se guarda el formulario
            messages.success(request, "Bicicleta subida correctamente") # mensaje a mostrar si la bicicleta se subio correctamente
            return redirect('messagebike') # si el formulario es almacenado se muestra la ventana con el mensaje de exito [messages.success]
    else:# si el formulario no es por metodo POST se muestra el formulario vacio al hacer submit
        form = BicicletasForm()
    return render(request, 'bike/uploadBike.html', {'form': form,'numcontratos':numcontratos,'nummensajes':nummensajes})





# Metodo para editar o actualizar una bicicleta subida por el usuario loguedo

class Editar_bicicleta(SuccessMessageMixin,LoginRequiredMixin, UpdateView):
    model = MiBicicleta # Modelo a usar 
    form_class = EditBicicletaForm # formulario a usar de forms.py
    template_name = 'bike/editar_bicicleta.html' # plantilla html a usar 
    success_url = reverse_lazy('perfil') # Si es correcto se regresa al perfil del usuario
    success_message='Los datos de tu bicicleta han sido cambiados correctamente!!' # Mensaje a mostrar si el post fue correcto







# función para eliminar la bicicleta del usuario en ventana de perfil
def delete_bike(request,id):
    bicicleta = MiBicicleta.objects.get(idmibicicleta = id) # se trae el id del objeto escogido
    if request.method == 'POST': # validaion del metodo solicitado
        bicicleta.estado = False # El estado de la bicicleta cambia de True a False
        bicicleta.save() # Se guarda el cambio en base de datos
        return redirect('perfil')   # Se redirecciona a la ventana de perfil
    return render(request,'pages/components/modals/modal_deleteBike.html',{'bicicleta':bicicleta}) # modal de mensaje de advertencia de eiminacion


# función para mostrar la vista de home y mostrar bicicletas en catalogo
def home(request):
    queryset = request.GET.get("Buscar")
    bicicletas = MiBicicleta.objects.filter(estado=True)

    # Condicion para mostrar la cantidad de contratos si el usuario esta logueado
    if request.user.is_authenticated:
        nummensajes = Contacto.objects.all().count()
        numcontratos = ContratoBicicleta.objects.filter(bicicleta__user=request.user).count() # Se trae la cantidad de contratos

        # Barra de busqueda para el usuario logueado
        if queryset :
            bicicletas = MiBicicleta.objects.filter(
                Q(user__last_name__icontains = queryset) | # Busqueda por apellido
                Q(user__first_name__icontains = queryset) | # Busqueda por nombre
                Q(precioalquiler__icontains = queryset) | # Busqueda por precio de alquiler
                Q(categoria__nombre__icontains= queryset) # Busqueda por categoria
            ).distinct()

        # Paginacion del catalogo
        paginator = Paginator(bicicletas, 9, 3)
        try:
            num = request.GET.get('list', '1')
            number = paginator.page(num)

        except PageNotAnInteger:
            number = paginator.page(1)

        except EmptyPage:
            number = paginator.page(paginator.num_pages)
        return render(request,'pages/inicio.html',{'page': number, 'paginator': paginator,'numcontratos':numcontratos,'nummensajes':nummensajes})

    if queryset :
        bicicletas = MiBicicleta.objects.filter(
            Q(user__last_name__icontains = queryset) | 
            Q(user__first_name__icontains = queryset) | 
            Q(precioalquiler__icontains = queryset) | 
            Q(categoria__nombre__icontains= queryset)
        ).distinct()

    # Se trae todos las bicicletas registradas en modelo de base de datod MIBicicleta
    # bicicletas = MiBicicleta.objects.filter()
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



# Funcion  para mostrar el template de menu de configuraciones del usuario
@login_required
def settings(request):

    nummensajes = Contacto.objects.all().count()
    numcontratos = ContratoBicicleta.objects.filter(bicicleta__user=request.user).count()

    return render(request, 'user/settingsuser.html',{'nummensajes':nummensajes,'numcontratos':numcontratos})

# Detalles de una biciclta al dar click sobre la imagen de la bici
class Descripcionbike(DetailView):
    model = MiBicicleta 
    template_name = 'pages/components/modals/modal_detailbike.html' # modal 


# filtro de  bicicletas Urbanas-------------------
def bikeurbanas(request):

    queryset = request.GET.get("Buscar")
    bicicletas = MiBicicleta.objects.filter(
        estado = True,
        categoria = Categoria.objects.get(nombre = 'Urbana')
    )
    # Condicion para mostrar la cantidad de contratos si el usuario esta logueado
    if request.user.is_authenticated:
        nummensajes = Contacto.objects.all().count()
        numcontratos = ContratoBicicleta.objects.filter(bicicleta__user=request.user).count() # Se trae la cantidad de contratos

        if queryset :
            bicicletas = MiBicicleta.objects.filter(
                Q(user__last_name__icontains = queryset) | # Busqueda por nombre
                Q(user__first_name__icontains = queryset) | # Busqueda por apellido
                Q(precioalquiler__icontains = queryset) | # Busqueda por precio de alquiler
                Q(categoria__nombre__icontains= queryset) # Busqueda por categoria
            ).distinct()

        paginator = Paginator(bicicletas, 12, 3)
        try:
            num = request.GET.get('list', '1')
            number = paginator.page(num)

        except PageNotAnInteger:
            number = paginator.page(1)

        except EmptyPage:
            number = paginator.page(paginator.num_pages)
        return render(request,'bike/filtros_categorias/bike_urbanas.html',{'page': number, 'paginator': paginator,'numcontratos':numcontratos,'nummensajes':nummensajes})

    
    if queryset :
        bicicletas = MiBicicleta.objects.filter(
            Q(user__last_name__icontains = queryset) | 
            Q(user__first_name__icontains = queryset) | 
            Q(precioalquiler__icontains = queryset) | 
            Q(categoria__nombre__icontains= queryset)
        ).distinct()

    return render(request ,'bike/filtros_categorias/bike_urbanas.html',{'page': bicicletas})




# filtro de  bicicletas de Ruta -------------------
def bikeruta(request):

    queryset = request.GET.get("Buscar")
    bicicletas = MiBicicleta.objects.filter(
        estado = True,
        categoria = Categoria.objects.get(nombre = 'Ruta')
    )



    if request.user.is_authenticated:
        nummensajes = Contacto.objects.all().count()
        numcontratos = ContratoBicicleta.objects.filter(bicicleta__user=request.user).count()

        if queryset :
            bicicletas = MiBicicleta.objects.filter(
                Q(user__last_name__icontains = queryset) | # Busqueda por apellido
                Q(user__first_name__icontains = queryset) | # Busqueda por nombre
                Q(precioalquiler__icontains = queryset) | # Busqueda por precio
                Q(categoria__nombre__icontains= queryset) # busqueda por categoria
            ).distinct()

        paginator = Paginator(bicicletas, 12, 3)
        try:
            num = request.GET.get('list', '1')
            number = paginator.page(num)

        except PageNotAnInteger:
            number = paginator.page(1)

        except EmptyPage:
            number = paginator.page(paginator.num_pages)
        return render(request,'bike/filtros_categorias/bike_ruta.html',{'page': number, 'paginator': paginator,'numcontratos':numcontratos,'nummensajes':nummensajes})
    
    if queryset :
        bicicletas = MiBicicleta.objects.filter(
            Q(user__last_name__icontains = queryset) | 
            Q(user__first_name__icontains = queryset) | 
            Q(precioalquiler__icontains = queryset) | 
            Q(categoria__nombre__icontains= queryset)
        ).distinct()

    return render(request ,'bike/filtros_categorias/bike_ruta.html',{'page': bicicletas})




# filtro de  bicicletas de Todo terreno -------------------
def biketodoterreno(request):
    queryset = request.GET.get("Buscar")
    bicicletas = MiBicicleta.objects.filter(
        estado = True,
        categoria = Categoria.objects.get(nombre = 'Todo terreno')
    )
    # 
    if request.user.is_authenticated:
        nummensajes = Contacto.objects.all().count()
        numcontratos = ContratoBicicleta.objects.filter(bicicleta__user=request.user).count()

        if queryset :
            bicicletas = MiBicicleta.objects.filter(
                Q(user__last_name__icontains = queryset) | # Busqueda por nombre
                Q(user__first_name__icontains = queryset) | # Busqueda por apellido
                Q(precioalquiler__icontains = queryset) | # Busqueda por precio
                Q(categoria__nombre__icontains= queryset) # Busqueda por categoria
            ).distinct()

        paginator = Paginator(bicicletas, 12, 3)
        try:
            num = request.GET.get('list', '1')
            number = paginator.page(num)

        except PageNotAnInteger:
            number = paginator.page(1)

        except EmptyPage:
            number = paginator.page(paginator.num_pages)
        return render(request,'bike/filtros_categorias/bike_todoterreno.html',{'page': number, 'paginator': paginator,'numcontratos':numcontratos,'nummensajes':nummensajes})


    if queryset :
        bicicletas = MiBicicleta.objects.filter(
            Q(user__last_name__icontains = queryset) | 
            Q(user__first_name__icontains = queryset) | 
            Q(precioalquiler__icontains = queryset) | 
            Q(categoria__nombre__icontains= queryset)
        ).distinct()

    return render(request ,'bike/filtros_categorias/bike_todoterreno.html',{'page': bicicletas})



# filto de bicicletas disponibles
def bikedisponibles(request):
    queryset = request.GET.get("Buscar")
    bicicletas = MiBicicleta.objects.filter(
        estado=True,
        disponible = True
    )

    if request.user.is_authenticated:
        nummensajes = Contacto.objects.all().count()
        numcontratos = ContratoBicicleta.objects.filter(bicicleta__user=request.user).count()

        if queryset :
            bicicletas = MiBicicleta.objects.filter(
                Q(user__last_name__icontains = queryset) | # Busqueda por nombre
                Q(user__first_name__icontains = queryset) | # Busqueda por apellido
                Q(precioalquiler__icontains = queryset) | # Busqueda por precio de aquiler
                Q(categoria__nombre__icontains= queryset) # Busqueda por categoria
            ).distinct()

        paginator = Paginator(bicicletas, 12, 3)
        try:
            num = request.GET.get('list', '1')
            number = paginator.page(num)

        except PageNotAnInteger:
            number = paginator.page(1)

        except EmptyPage:
            number = paginator.page(paginator.num_pages)
        return render(request,'bike/filtros_categorias/bike_disponibles.html',{'page': number, 'paginator': paginator,'numcontratos':numcontratos,'nummensajes':nummensajes})


    if queryset :
        bicicletas = MiBicicleta.objects.filter(
            Q(user__last_name__icontains = queryset) | 
            Q(user__first_name__icontains = queryset) | 
            Q(precioalquiler__icontains = queryset) | 
            Q(categoria__nombre__icontains= queryset)
        ).distinct()

    return render(request ,'bike/filtros_categorias/bike_disponibles.html',{'page': bicicletas})


class ContratoBicicletaView(CreateView):
    model: MiBicicleta
    form_class = ContratoBicicletaForm # Formulario creado en forms.py
    template_name ='pages/contrato.html'

    def form_valid(self, form):
        current_user = get_object_or_404(User, pk=self.request.user.pk) # Guarda en el modelo contrato la llave pimaria del usuario logueado(auntenticado)
        current_bici = MiBicicleta.objects.filter(pk=self.kwargs.get('pk')).first() # Guarda en el modelo contrato la llave primaria de la biciclta seleccionada
        bici = form.save(commit=False) # Necesario para traer la instancias del modelo user y mibicicleta
        bici.user = current_user # lleno el campo de user(arrendatario) automaticamente para que se almacena en la tabla  
        bici.bicicleta = current_bici # lleno el campo con la pk de la bicicleta seleccionada automaticamente y se guarda en la tabla
        bici.save() # Se guarda el formulario
        return redirect('downloadcontrato') # Si el formulario es correcto se pasa a descargar el contrato    


    # Funcion para retornar un diccionario de variables a utilizar  en el template
    def get_context_data(self, **kwargs):
        context = super(ContratoBicicletaView, self).get_context_data(**kwargs)
        context['object'] = MiBicicleta.objects.filter(pk=self.kwargs.get('pk')).first()
        context['nummensajes'] = Contacto.objects.all().count()
        context['numcontratos'] = ContratoBicicleta.objects.filter(bicicleta__user=self.request.user).count()
        return context

# ---------------------------------------------------------------------------------------------



# Descargar contrato en formato pdf
class ContratoPdf(LoginRequiredMixin,View):

    # funcion para mostrar imagenes en el pdf
    def link_callback(self, uri, rel):

        # variables de archivos usados
        sUrl = STATIC_URL  # archivos estaticos
        sRoot = STATIC_ROOT  
        mUrl = MEDIA_URL  # archivos de la carpeta media
        mRoot = MEDIA_ROOT  

        # convertir URLS en rutas absolutas del sistema
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri  

        # Se asegura que archivo a mostrar exista
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    # funcio para mostrar y personalizar la vista del pdf
    def get(self,request,*args,**kwargs):
        try:
            # Template donde se va a mostrar el pde
            template = get_template('contrato/contratopdf.html')
            context={
                # diccionario de variables para usar en el template
                'contrato': ContratoBicicleta.objects.get(pk=self.kwargs['pk']), # llave primaria del contrato creado  
                'icon': 'static/img/iconsBiken/icono.png' # imagen del icono biken a mostrar en la plantilla del pdf
                }
            html=template.render(context) # Codigo html creado
            response = HttpResponse(content_type='application/pdf') # del codigo html a formato pdf
            response['Content-Disposition']='attachment;filename="contratoBiken.pdf"' # Descarga el contrato de una vez, si se quita esta linea se visualiza el pdf al instante para despues ser descargado
            pisaStatus =pisa.CreatePDF(
                html,dest=response, # se trae la construccion del html
                link_callback=self.link_callback, # se trae la funcion de archivos de imagenes para ser mostrados
            )
            # Si hay algun error en la creacion del html muestro un mensaje de error en pantalla
            if pisaStatus.err:
                return HttpResponse('Tienes algunos errores <pre>' + html + '</pre>')
            return response
        except:
            pass
        # con el try catch su hay un error al mostrar el  se redirecciona a la ventana de inicio principal
        return HttpResponseRedirect(reverse_lazy('home'))

# Vista de contratos en formato pdf 
class ContratoPdftoProfile(LoginRequiredMixin,View):

    def link_callback(self, uri, rel):

        # use short variable names
        sUrl = STATIC_URL  # Typically /static/
        sRoot = STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = MEDIA_URL  # Typically /static/media/
        mRoot = MEDIA_ROOT  # Typically /home/userX/project_static/media/

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path


    def get(self,request,*args,**kwargs):
        try:
            template = get_template('contrato/contratopdf.html')
            context={
                'contrato': ContratoBicicleta.objects.get(pk=self.kwargs['pk']),
                'icon': 'static/img/iconsBiken/icono.png'
                }
            html=template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition']='attachment;filename="contratoBiken.pdf"'
            pisaStatus =pisa.CreatePDF(
                html,dest=response,
                link_callback=self.link_callback,
            )
            if pisaStatus.err:
                return HttpResponse('Tienes algunos errores <pre>' + html + '</pre>')
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('home'))


# funcion para descargar el contrato despues de ser validado el contrato
@login_required
def downloadpdf(request):
    contrato = ContratoBicicleta.objects.last() # Traigo el ultimo contrato creado
    return render(request,'contrato/download_contrato.html',{'contrato':contrato})


# funcion para ver la lista de contratos en el perfil o en el icono de  notificaciones 
@login_required
def listContratos(request):
    contratoUser = ContratoBicicleta.objects.filter(bicicleta__user=request.user)
    return render(request,'pages/components/modals/modal_contratos.html',{'contratoUser':contratoUser})



# metodo para mostrar la vista de contacto con Biken al usuario
class ContactoView(SuccessMessageMixin,CreateView):
    model = Contacto
    template_name = 'pages/contacto.html'
    form_class = ContactoForm
    success_url = reverse_lazy('contacto')
    success_message='Gracias por contactarse con Biken'

    
    def get_context_data(self, **kwargs):
        context = super(ContactoView, self).get_context_data(**kwargs)
        context['nummensajes'] = Contacto.objects.all().count()
        context['numcontratos'] = ContratoBicicleta.objects.filter(bicicleta__user=self.request.user).count()
        return context
    


# funcion para ver la lista de mensajes del formulario contacto
@login_required
def messagesContacto(request):
    message = Contacto.objects.all()
    return render(request,'pages/components/modals/modal_messages.html',{'message':message})

