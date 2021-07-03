from django.conf.urls import include 
from django.conf.urls.static import static # mostrar imagenes en las vistas
from django.conf import settings
from django.urls import path
from Apps.usuario import views # se traen los metodos hechos para mostrar las vistas en el archivo views.py


urlpatterns = [
    # user
    path('login/',views.login,name='login'),# url de la vista del login de usuarios registrados en Biken
    path('registro/',views.registro, name='registro'),# url de la vista del  registro de usuarios para hacer parte de Biken
    path('profile/',views.profileUser,name='perfil'),# url de la vista de  perfil de usuarios registrados
    path('profile/<str:username>/',views.profileUser,name='perfil'),# url de perfiles de usuarios con parametro de username
    path('profile/settings/editprofile/',views.ProfileUpdate.as_view(),name='editprofile'),# url de la vista de edicion de perfil de usuarios registrados
    path('profile/settings/editemail',views.EmailUpdate.as_view(),name='editemail'),# url de la vista de edicion de email de usuarios registrados
    path('profile/settings/edituser',views.UserUpdate.as_view(),name='edituser'),
    path('accounts/',include('django.contrib.auth.urls')),# url mostrada como complemento para el login y registro generados por Django

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  # Mostrar imagenes 

