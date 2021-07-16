from django.db.models import query
from rest_framework import viewsets
from django.contrib.auth.models import User

from .serializer import *
from .models import *




class RegisterViewset(viewsets.ModelViewSet):
    queryset =  User.objects.all()
    serializer_class = RegisterSerializer


    

class BicicletaViewset(viewsets.ModelViewSet):
    queryset = MiBicicleta.objects.all()
    serializer_class = BicicletaSerializer


class UsersViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer


class ProfileViewset(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = ProfileSerializer


class ContratoViewset(viewsets.ModelViewSet):
    queryset = Contrato.objects.all()
    serializer_class = ContratoSerializer


class CategoriaBikeViewset(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaBikeSerializer


class MaterialBikeViewset(viewsets.ModelViewSet):
    queryset= Materialbicicletas.objects.all()
    serializer_class = MaterialBikeSerializer



