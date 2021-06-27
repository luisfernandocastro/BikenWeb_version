"""BikenPro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import include 
from django.conf.urls.static import static # mostrar imagenes en las vistas
from django.contrib import admin # Mostrar las vistas de administracion del sitio web
from django.urls import path
from django.conf import settings
from Apps.principal import views # se traen los metodos hechos para mostrar las vistas en el archivo views.py


urlpatterns = [
    path('jet/', include('jet.urls', 'jet')), # url para el admin con el diseño de la libreria de jet_django
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('managementBiken/', admin.site.urls), 
    path('',views.index,name ='index'),# url de la vista index del sitio web
    path('home/',views.home,name ='home'), # url de la vista del  inicio de la pogina y catalogo del sitio
    path('registro/',views.registro, name='registro'),# url de la vista del  registro de usuarios para hacer parte de Biken
    path('login/',views.login, name='login'),# url de la vista del login de usuarios registrados en Biken
    path('profile/',views.profileUser,name='perfil'),# url de la vista de  perfil de usuarios registrados
    path('profile/<str:username>/',views.profileUser,name='perfil'),# url de perfiles de usuarios con parametro de username
    path('editprofile/',views.ProfileUpdate.as_view(),name='editprofile'),# url de la vista de edicion de perfil de usuarios registrados
    path('uploadBike/' , views.uploadBike, name='uploadbike'),# url de la vista de  formulario de subir bicicletas por los usuarios
    path('editBike/<int:id>/' , views.editar_bicicleta, name='editar_bicicleta'),# url de la vista de  edicion de bicicletas del  usuario si ha subido bicicletas
    path('registrocorrecto/' , views.messageRegistro, name='messagereg'),# url de la vista de mensaje de registro exitoso
    path('subidabicicorrecta/' , views.messageUploadBike, name='messagebike'),# url de la vista de  mensaje de bicicleta subida correctamente
    path('quienessomos/' , views.quienesSomos, name='quienessomos'),# url de la vista de  informacion respecto a Biken
    path('contacto/' ,views.contacto, name='contacto'),# url de la vista del formulario de contacto para comunicacion con nosotros
    path('accounts/',include('django.contrib.auth.urls')),# url mostrada como complemento para el login y registro generados por Django

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  # Mostrar imagenes 
