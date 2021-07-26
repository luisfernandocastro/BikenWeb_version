from typing import Reversible
from django import forms
import django
from django import http
from django.contrib.messages import views
from django.db.models import query
from django.http.response import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.urls.base import reverse
from django.urls.conf import path
from django.views.generic import DeleteView
from django.urls import reverse_lazy  # redireccion de funciones
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormMixin, FormView, UpdateView
from .models import *  # se traen todas las tablas del modelo de base de datos
# importaciones del archivo forms.py
from .forms import BicicletasForm,EditBicicletaForm,ContratoBicicletaForm
# se muestran los mensajes apartir de una accion de un formulario...etc
from django.contrib import messages
# importacion del modelo usuario personalizado para ser utilizado en vez del que viene por defecto
from django.contrib.auth import get_user_model
# decorador para solicitar el login de un usuario para ver una vista no permitida sin loguearse
from django.contrib.auth.decorators import login_required
# Actualiaciones  o ediciones de datos que se encuentran en la base de datos generadas por Django
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin

#importaciones pdf------------

import os
from django.http import HttpResponse
from django.conf.global_settings import STATIC_ROOT,STATIC_URL,MEDIA_ROOT,MEDIA_URL
from django.conf import settings
from django.template import Context, context
from django.template.loader import get_template 
from xhtml2pdf import pisa

# end importaciones pdf-------

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
            messages.success(request, "Bicicleta subida correctamente")
            return redirect('messagebike')
    else:
        form = BicicletasForm()
    return render(request, 'bike/uploadBike.html', {'form': form})





# -------metodo para editar o actualizar una bicicleta subida por el usuario loguedo

class Editar_bicicleta(SuccessMessageMixin,LoginRequiredMixin, UpdateView):
    model = MiBicicleta
    form_class = EditBicicletaForm
    template_name = 'bike/editar_bicicleta.html'
    success_url = reverse_lazy('perfil')
    success_message='Los datos de tu bicicleta han sido cambiados correctamente!!'

# class Editar_bicicleta(SuccessMessageMixin,UpdateView):
#     model = MiBicicleta
#     form_class = BicicletasForm
#     template_name = 'bike/editar_bicicleta.html'
#     success_url = reverse_lazy('perfil')



# def editar_bicicleta(request, id):

#     bicicleta = get_object_or_404(MiBicicleta, idmibicicleta=id)

#     data = {
#         'form': BicicletasForm(instance=bicicleta)
#     }

#     if request.method == 'POST':
#         formulario = BicicletasForm(
#             data=request.POST, instance=bicicleta, files=request.FILES)
#         if formulario.is_valid():
#             formulario.save()
#             return redirect(to='perfil')
#         data['form'] = BicicletasForm(
#             instance=bicicleta.objects.get(idmibicicleta=id))

#     return render(request, 'bike/editar_bicicleta.html', data)




class Delete_bicicleta(DeleteView):
    model = MiBicicleta
    template_name = 'pages/components/modal_deleteBike.html'
    success_url = reverse_lazy('perfil')



# metodo para mostrar la vista de home y mostrar bicicletas en catalogo
def home(request):


    queryset = request.GET.get("Buscar")
    bicicletas = MiBicicleta.objects.all()
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




@login_required
def settings(request):
    return render(request, 'user/settingsuser.html')


class Descripcionbike(DetailView):
    model = MiBicicleta
    template_name = 'pages/components/modal_detailbike.html'


def bikeurbanas(request):

    queryset = request.GET.get("Buscar")
    bicicletas = MiBicicleta.objects.filter(
        categoria = Categoria.objects.get(nombre = 'Urbana')
    )
    if queryset :
        bicicletas = MiBicicleta.objects.filter(
            Q(user__last_name__icontains = queryset) | 
            Q(user__first_name__icontains = queryset) | 
            Q(precioalquiler__icontains = queryset) | 
            Q(categoria__nombre__icontains= queryset)
        ).distinct()

    return render(request ,'bike/filtros_categorias/bike_urbanas.html',{'page': bicicletas})


def bikeruta(request):

    queryset = request.GET.get("Buscar")
    bicicletas = MiBicicleta.objects.filter(
        categoria = Categoria.objects.get(nombre = 'Ruta')
    )
    if queryset :
        bicicletas = MiBicicleta.objects.filter(
            Q(user__last_name__icontains = queryset) | 
            Q(user__first_name__icontains = queryset) | 
            Q(precioalquiler__icontains = queryset) | 
            Q(categoria__nombre__icontains= queryset)
        ).distinct()

    return render(request ,'bike/filtros_categorias/bike_ruta.html',{'page': bicicletas})


def biketodoterreno(request):

    queryset = request.GET.get("Buscar")
    bicicletas = MiBicicleta.objects.filter(
        categoria = Categoria.objects.get(nombre = 'Todo terreno')
    )
    if queryset :
        bicicletas = MiBicicleta.objects.filter(
            Q(user__last_name__icontains = queryset) | 
            Q(user__first_name__icontains = queryset) | 
            Q(precioalquiler__icontains = queryset) | 
            Q(categoria__nombre__icontains= queryset)
        ).distinct()

    return render(request ,'bike/filtros_categorias/bike_todoterreno.html',{'page': bicicletas})




def bikedisponibles(request):

    queryset = request.GET.get("Buscar")
    bicicletas = MiBicicleta.objects.filter(
        disponible = True
    )
    if queryset :
        bicicletas = MiBicicleta.objects.filter(
            Q(user__last_name__icontains = queryset) | 
            Q(user__first_name__icontains = queryset) | 
            Q(precioalquiler__icontains = queryset) | 
            Q(categoria__nombre__icontains= queryset)
        ).distinct()

    return render(request ,'bike/filtros_categorias/bike_todoterreno.html',{'page': bicicletas})



# class ContratoBicicleta(CreateView):
#     template_name = 'pages/contrato.html'
#     model = Contrato
#     form_class = ContratoBicicletaForm
#     success_url = reverse_lazy('home')


# class DetailBikeContrato(DetailView):
#     model = MiBicicleta
#     template_name = 'pages/contrato.html'

# class Contrato(CreateView, DetailView):
#     template_name = 'pages/contrato.html'
#     model = Contrato
#     form_class = ContratoBicicletaForm
#     success_url = reverse_lazy('home')



#--------------------------------------------------------

class ContratoBicicletaView(LoginRequiredMixin,CreateView,DetailView):
    model = MiBicicleta
    form_class =ContratoBicicletaForm
    template_name = 'pages/contrato.html'
    success_url = reverse_lazy('contratobike')


    def form_valid(self, form):
        current_user = get_object_or_404(User, pk=self.request.user.pk)
        current_bici = MiBicicleta.objects.filter(pk=self.kwargs.get('pk')).first()

        # current_bici = get_object_or_404(MiBicicleta, pk=self.request.object.pk)
        bici = form.save(commit=False)
        bici.user = current_user
        bici.bicicleta = current_bici
        bici.save()
        messages.success(self.request, "Contrato correcto")
        return redirect('downloadcontrato')


    
# -------------------------------------------------------

    # success_url = reverse_lazy('home')

    # def form_valid(self, form):
    #     print ('happening2')
    #     MiBicicleta.disponible=False
    #     return http.HttpResponse("form ism valid.. this is just an HttpResponse object")

    # def form_invalid(self, form):
    #     print ("form is invalid")
    #     return http.HttpResponse("form is invalid.. this is just an HttpResponse object")

# class ContratoBicicletadetailView(DetailView):
#     model = MiBicicleta
#     template_name = 'pages/contrato.html'

    # def get_context_data(self, **kwargs):
    #     context = super(ContratoBicicleta, self).get_context_data(**kwargs)
    #     context['form'] = self.get_form()
    #     return context

    # def post(self, request, *args, **kwargs):
    #     return CreateView.post(self, request, *args, **kwargs)



# @login_required
# def contratoBicicleta(request):
#     current_user = get_object_or_404(User, pk=request.user.pk)
#     # current_bici = get_object_or_404(MiBicicleta,idmibicicleta = object.idmibicicleta)
#     if request.method == 'POST':
#         # request.FILES ,necesario para subir imagenes
#         form = ContratoBicicletaForm(request.POST, files=request.FILES)
#         if form.is_valid():
#             bici = form.save(commit=False)
#             bici.user = current_user
#             # bici.bicicleta = current_bici
#             bici.save()
#             messages.success(request, "Contrato correcto")
#             return redirect('home')
#     else:
#         form = ContratoBicicletaForm()
#     return render(request, 'pages/contrato.html', {'form': form})


# -------------------*-------------*-----------------------*-------------*-




# class ContratoBicicleta(LoginRequiredMixin,DetailView):
#     model=ContratoBicicleta
#     succes_url=reverse_lazy('home')

#     def post(self,request,*args,**kwargs):
#         if request.is_ajax():
#             bicicleta = MiBicicleta.objects.filter(id=request.POST.get('bicicleta')).first()
#             user = request.user.objects.filter(id=request.POST.get('user')).first()
#             if bicicleta and user:
#                 nuevo_contrato= self.model(
#                     bicicleta=bicicleta,
#                     user=user
#                 )
#                 nuevo_contrato.save()
#                 mensaje = f'(self.model.__name__) registrada correctamente'
#                 error = 'No hay error'
#                 response=JsonResponse({'mensaje':mensaje,'error':error,'url':self.success_url})
#                 response.status_code=201
#                 return response
#         return redirect('home')



class ContratoPdf(View):

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
        # try:
        template = get_template('contrato/contratopdf.html')
        context={
            'contrato': ContratoBicicleta.objects.get(pk=self.kwargs['pk']),
            'icon': 'static/img/iconsBiken/icono.png'
            }
        html=template.render(context)
        response = HttpResponse(content_type='application/pdf')
        # response['Content-Disposition']='attachment;filename="report.pdf"'
        pisaStatus =pisa.CreatePDF(
            html,dest=response,
            link_callback=self.link_callback,
        )
        if pisaStatus.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
        # except:
        #     pass
        # return HttpResponseRedirect(reverse_lazy('home'))


def downloadpdf(request):
    contrato = ContratoBicicleta.objects.last()
    return render(request,'contrato/download_contrato.html',{'contrato':contrato})