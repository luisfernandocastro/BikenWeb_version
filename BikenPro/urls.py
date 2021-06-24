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

import django
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf import settings
from Apps.principal import views 


urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('admin/', admin.site.urls), 
    path('',views.index,name ='index'),
    path('home/',views.home,name ='home'),
    path('registro/',views.registro, name='registro'),
    path('login/',views.login, name='login'),
    path('profile/',views.profileUser,name='perfil'),
    path('profile/<str:username>/',views.profileUser,name='perfil'),
    path('uploadBike/' , views.uploadBike, name='uploadbike'),
    path('editBike/<int:id>/' , views.editar_bicicleta, name='editar_bicicleta'),
    path('registrocorrecto/' , views.messageRegistro, name='messagereg'),
    path('subidabicicorrecta/' , views.messageUploadBike, name='messagebike'),
    path('quienessomos/' , views.quienesSomos, name='quienessomos'),
    path('contacto/' ,views.contacto, name='contacto'),
    path('accounts/',include('django.contrib.auth.urls')),
    path('editprofile/',views.ProfileUpdate.as_view(),name='editprofile')

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) 
