from django import db
from django.db import models
from django.db.models.fields.related import OneToOneField
from django.urls.base import reverse
from BikenPro.settings import MEDIA_URL, STATIC_URL
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, RegexValidator
from django.utils import timezone
from .validators import *
User=get_user_model()




# (Funciones en las que se reemplazara la imagen anterior, optimizando espacio)------->

# imagenes de perfil subidas por los usuarios
def custom_upload_to_profile(instance, filename):
    old_instance = Perfil.objects.get(pk=instance.pk)
    old_instance.image_user.delete()
    return 'user/profile/' + filename


# imagenes de portada subidas por los usuarios
def custom_upload_to_banner(instance, filename):
    old_instance = Perfil.objects.get(pk=instance.pk)
    old_instance.image_portada.delete()
    return 'user/banner/' + filename

# ----------------------------------------------------------------------------------->


# perfil de los usuarios regstrados    
class Perfil(models.Model):
    user=  models.OneToOneField(User,on_delete=models.CASCADE) # Relacion de uno a uno con el usuario
    telefono = models.CharField(db_column='Telefono',null=True,blank=True, max_length=7,validators=[MinLengthValidator(7)]) 
    direccion = models.CharField(db_column='Direccion', max_length=50,null=True,blank=True)
    estado = models.CharField(db_column='Biografia', max_length=80,null=True,blank=True) 
    image_portada = models.ImageField(upload_to='custom_upload_to_banner',null=True,blank=True,verbose_name='Imagen de portada')
    image_user = models.ImageField(upload_to='custom_upload_to_profile',null=True,blank=True,verbose_name='Imagen de perfil')

    # Cambia el object(0)
    def __str__(self):  
        return f'Perfil de {self.user.username}'

    # funcion para guardar la imagen de perfil en la ruta especificada
    def get_image(self):
        if self.image_user:
            return '{}{}'.format(MEDIA_URL,self.image_user)
        return '{}{}'.format(STATIC_URL,'img/imgs_plus/user.png')
    
    # funcion para guardar la imagen de portada en la ruta especificada
    def get_imagePortada(self):
        if self.image_portada:
            return '{}{}'.format(MEDIA_URL,self.image_portada)
        return '{}{}'.format(STATIC_URL,'img/imgs_plus/banner.jpg')
    

    class Meta:
        # Nombre general de la tabla a mostrar en el panel de administracion
        verbose_name_plural='Perfiles de usuarios'



# Valoidacion del campo decripcion de la bicicleta 
validatorDescription = RegexValidator(r"^[a-zA-ZÀ-ÿ0-9\s]{1,40}$","La descripcion de tu Bici no puede contener caracteres especiales")

# Datos de las bicicletas
class MiBicicleta(models.Model):
    idmibicicleta = models.BigAutoField(db_column='idmibicicleta',primary_key=True, serialize=False, verbose_name='ID')
    user=models.ForeignKey(User,db_column='Propietario', on_delete=models.CASCADE,related_name='miBici',null=True)
    disponible = models.BooleanField(db_column='Disponible',default=True)
    marca = models.CharField(db_column='Marca', max_length=45,default=None)  
    color = models.CharField(db_column='Color', max_length=50,default=None)  
    material = models.ForeignKey('Materialbicicletas', models.DO_NOTHING, db_column='Material',default=None)  
    timestamp=models.DateTimeField(db_column='Fecha de subida',default=timezone.now)
    categoria = models.ForeignKey('Categoria', models.DO_NOTHING, db_column='Categoria',default=None)  
    precioalquiler = models.DecimalField(db_column='PrecioAlquiler', max_digits=6, decimal_places=3,verbose_name='Precio Alquiler',default=None)  
    valortiempohoras= models.IntegerField(db_column='Horas de alquiler',null=True,blank=True,default=0)
    valortiempomin= models.IntegerField(db_column='Minutos de alquiler',null=True,blank=True,default=0)
    descripcionbici = models.TextField(db_column='DescripcionBici', max_length=150,null=True,default=None,blank=True,validators=[validatorDescription]) 
    foto = models.ImageField(db_column='Foto', max_length=100, null=True)  
    estado = models.BooleanField(db_column='estado',default=True)


    class Meta:
        ordering=['-timestamp']
        verbose_name_plural='Bicicletas'
    
    def __str__(self):
        return f'{self.user.username}'




class Catalogo(models.Model):
    idcatalogo = models.AutoField(db_column='idCatalogo', primary_key=True)  
    bicicleta = models.ForeignKey(MiBicicleta, models.DO_NOTHING, db_column='Bicicleta')  
    fechahorasubida = models.DateTimeField(db_column='fechaHoraSubida')  

    class Meta:
        managed = False
        db_table = 'catalogo'
        verbose_name_plural='Catalogo' 

# Eleccion de categoria de  bicicleta
class Categoria(models.Model):
    idmodelo = models.AutoField(db_column='idModelo', primary_key=True)  
    nombre = models.CharField(db_column='Nombre', max_length=45)  

    class Meta:
        managed = False
        db_table = 'categoria'
        verbose_name_plural='Categoria' 


    def __str__(self):
        return self.nombre

# importacion en datetime para calcular fechas y horas exactas
from datetime import datetime, timedelta

datenow = datetime.now() # Fecha y  ahora actual

opcionesdocumento=[
    [0,'Cédula de Ciudadania'],
    [1,'Carnet de Extranjeria'],
]

class ContratoBicicleta(models.Model):
    fechainicio=models.DateTimeField(db_column='Fecha Inicio Contrato',default=datetime.now)
    fechafin=models.DateTimeField(db_column='fechafin',default=datenow+timedelta(hours=48))
    tipodocumento=models.IntegerField(db_column='Tipo de Documento',choices=opcionesdocumento,default=0)
    numerodocumento=models.BigIntegerField(db_column='Numero Documento',default=None)
    direccion=models.CharField(db_column='Direccion',null=True,blank=True,max_length=45)
    horainicio = models.TimeField(db_column='Hora inicio',default=None)  
    horafin=models.TimeField(db_column='Hora fin',default=None)
    tipocontrato = models.ForeignKey('Tipocontrato', models.DO_NOTHING, db_column='Tipocontrato',default=1)  
    user=models.ForeignKey(User,db_column='Arrendatario', on_delete=models.CASCADE,related_name='bicicleta',null=True)
    bicicleta = models.ForeignKey(MiBicicleta, models.DO_NOTHING, db_column='Bicicleta',null=True)  
    estado = models.BooleanField(db_column='estado',default=True)


    class Meta:
        verbose_name_plural='Contratos'
    
    def get_absolute_url(self):
        return reverse('home', args=[self.id])




class FotoPerfiluser(models.Model):
    idfotouser = models.AutoField(db_column='idfotoUser', primary_key=True)  
    foto = models.CharField(max_length=100)
    usuario_idusuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='Usuario_idUsuario')  

    class Meta:
        managed = False
        db_table = 'foto_perfiluser'
        verbose_name_plural='Foto perfil Usuario'

# opciones de materiales de la bicicleta
class Materialbicicletas(models.Model):
    idmaterialbicicletas = models.AutoField(db_column='idMaterialBicicletas', primary_key=True)  
    nombre = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'materialbicicletas'
        verbose_name_plural='Material Bicicletas'

    def __str__(self):
        return self.nombre




class Perfilusuario(models.Model):
    idroles = models.AutoField(db_column='idRoles', primary_key=True)  
    nombre = models.CharField(db_column='Nombre', max_length=45)  
    descripcionrol = models.TextField(db_column='descripcionRol', blank=True, null=True)  
    usuario_idusuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='Usuario_idUsuario')  

    class Meta:
        managed = False
        db_table = 'perfilusuario'
        verbose_name_plural='Perfil Usuario' 


class Persona(models.Model):
    idpersona = models.AutoField(db_column='idPersona', primary_key=True)  
    nombres = models.CharField(db_column='Nombres', max_length=50)  
    apellidos = models.CharField(db_column='Apellidos', max_length=50)  
    numidentificacion = models.BigIntegerField(db_column='NumIdentificacion')  
    numcelular = models.BigIntegerField(db_column='NumCelular')  
    numtelefono = models.BigIntegerField(db_column='NumTelefono', blank=True, null=True)  
    correoelectronico = models.CharField(db_column='CorreoElectronico', max_length=45)  

    class Meta:
        managed = False
        db_table = 'persona'
        verbose_name_plural='Persona' 


    def __str__(self):
        cadenaName = self.nombres + ' ' + self.apellidos
        return cadenaName



class Privilegios(models.Model):
    idprivilegios = models.AutoField(db_column='idPrivilegios', primary_key=True)  
    privilegio = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'privilegios'


class Reserva(models.Model):
    idreserva = models.AutoField(db_column='idReserva', primary_key=True)  
    bicicleta = models.ForeignKey(MiBicicleta, models.DO_NOTHING, db_column='Bicicleta')  
    disponibleen = models.TimeField(db_column='DisponibleEn', blank=True, null=True)  
    disponible = models.CharField(db_column='Disponible', max_length=2)  

    class Meta:
        managed = False
        db_table = 'reserva'
        verbose_name_plural='Reserva' 


class Tiempoprestamo(models.Model):
    idtiempodisponibilidad = models.IntegerField(db_column='idTiempoDisponibilidad', primary_key=True)  
    bicicletas_idbicicletas = models.ForeignKey(MiBicicleta, models.DO_NOTHING, db_column='Bicicletas_idBicicletas')  
    contrato_idcontrato = models.ForeignKey(ContratoBicicleta, models.DO_NOTHING, db_column='Contrato_idContrato')  
    tiempoinicio = models.CharField(db_column='tiempoInicio', max_length=45, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'tiempoprestamo'
        verbose_name_plural='Tiempo Prestamo'


class Tipocontrato(models.Model):
    idtipocontrato = models.AutoField(db_column='idtipocontrato', primary_key=True)  
    nombre = models.CharField(db_column='Nombre', max_length=45)  
    descripcion = models.CharField(db_column='Descripcion', max_length=45, blank=True, null=True)  

    class Meta:
        db_table = 'tipocontrato'
        verbose_name_plural='Tipo contrato'
        managed = False

    def __str__(self):
        return self.nombre 

class Usuario(models.Model):
    idusuario = models.AutoField(db_column='idUsuario', primary_key=True)  
    usuario = models.CharField(db_column='Usuario', max_length=20)  
    password = models.CharField(db_column='Password', max_length=100)  
    persona_idpersona = models.ForeignKey(Persona, models.DO_NOTHING, db_column='Persona_idPersona')  

    class Meta:
        managed = False
        db_table = 'usuario'




tiposcontacto = [
    [0,'Dudas'],
    [1,'Queja'],
    [2,'Reclamo'],
    [3,'Denuncias'],
    [4,'Sugerencias'],
    [5,'Felicitación']
]


class Contacto(models.Model):
    name = models.CharField(max_length=100,db_column="Nombres y Apellidos")
    tipo = models.IntegerField(choices=tiposcontacto,null=True)
    asunto = models.CharField(max_length=100,db_column="Asunto",null=True)
    email = models.EmailField(max_length=120,db_column="Email")
    mensaje = models.TextField(max_length=500,db_column="Mensaje", validators=[validatortextarea])
    datetimemsg=models.DateTimeField(db_column='Fecha del mensaje', default=datetime.now)


    class Meta:
        verbose_name_plural = 'Mensajes de Usuarios'