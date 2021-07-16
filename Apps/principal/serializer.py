
from django.db.models import fields
from django.db.models.base import Model
from django.forms.models import fields_for_model
from rest_framework.schemas.coreapi import field_to_schema
from .models import *
from rest_framework import serializers
from django.contrib.auth  import get_user_model

User = get_user_model()


class BicicletaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiBicicleta
        fields = '__all__'




class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'




class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = '__all__'



class ContratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contrato
        fields = '__all__'


class CategoriaBikeSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Categoria
        fields = '__all__'


class MaterialBikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materialbicicletas
        fields= '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','password']
