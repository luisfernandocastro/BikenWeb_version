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


    
class Perfil(models.Model):
    user=  models.OneToOneField(User,on_delete=models.CASCADE)
    telefono = models.CharField(db_column='Telefono',null=True,blank=True, max_length=7,validators=[MinLengthValidator(7)])
    direccion = models.CharField(db_column='Direccion', max_length=50,null=True,blank=True)
    estado = models.CharField(db_column='Biografia', max_length=80,null=True,blank=True) 
    image_portada = models.ImageField(upload_to='custom_upload_to_banner',null=True,blank=True,verbose_name='Imagen de portada')
    image_user = models.ImageField(upload_to='custom_upload_to_profile',null=True,blank=True,verbose_name='Imagen de perfil')

    def __str__(self):  
        return f'Perfil de {self.user.username}'

    def get_image(self):
        if self.image_user:
            return '{}{}'.format(MEDIA_URL,self.image_user)
        return '{}{}'.format(STATIC_URL,'img/imgs_plus/user.png')
    
    def get_imagePortada(self):
        if self.image_portada:
            return '{}{}'.format(MEDIA_URL,self.image_portada)
        return '{}{}'.format(STATIC_URL,'img/imgs_plus/banner.jpg')
    
    class Meta:
        verbose_name_plural='Perfiles de usuarios'


# opcionesCategorias=[
#     [0,'Todo terreno'],
#     [1,'Urbana'],
#     [2,'Ruta']
# ]

validatorDescription = RegexValidator(r"^[a-zA-ZÀ-ÿ0-9\s]{1,40}$","La descripcion de tu Bici no puede contener caracteres especiales")


class MiBicicleta(models.Model):
    idmibicicleta = models.BigAutoField(db_column='idmibicicleta',primary_key=True, serialize=False, verbose_name='ID')
    user=models.ForeignKey(User,db_column='Propietario', on_delete=models.CASCADE,related_name='miBici',null=True)
    disponible = models.BooleanField(db_column='Disponible',default=True)
    marca = models.CharField(db_column='Marca', max_length=45,default=None)  # Field name made lowercase.
    color = models.CharField(db_column='Color', max_length=50,default=None)  # Field name made lowercase.
    material = models.ForeignKey('Materialbicicletas', models.DO_NOTHING, db_column='Material',default=None)  # Field name made lowercase.
    timestamp=models.DateTimeField(db_column='Fecha de subida',default=timezone.now)
    categoria = models.ForeignKey('Categoria', models.DO_NOTHING, db_column='Categoria',default=None)  # Field name made lowercase.
    precioalquiler = models.DecimalField(db_column='PrecioAlquiler', max_digits=6, decimal_places=3,verbose_name='Precio Alquiler',default=None)  # Field name made lowercase.
    valortiempohoras= models.IntegerField(db_column='Horas de alquiler',null=True,blank=True,default=0)
    valortiempomin= models.IntegerField(db_column='Minutos de alquiler',null=True,blank=True,default=0)
    descripcionbici = models.TextField(db_column='DescripcionBici', max_length=150,null=True,default=None,blank=True,validators=[validatorDescription]) 
    foto = models.ImageField(db_column='Foto', max_length=100, null=True)  # Field name made lowercase.
    estado = models.BooleanField(db_column='estado',default=True)


    class Meta:
        ordering=['-timestamp']
        verbose_name_plural='Bicicletas'
    
    def __str__(self):
        return f'{self.user.username}'




class Catalogo(models.Model):
    idcatalogo = models.AutoField(db_column='idCatalogo', primary_key=True)  # Field name made lowercase.
    bicicleta = models.ForeignKey(MiBicicleta, models.DO_NOTHING, db_column='Bicicleta')  # Field name made lowercase.
    fechahorasubida = models.DateTimeField(db_column='fechaHoraSubida')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'catalogo'
        verbose_name_plural='Catalogo' 


class Categoria(models.Model):
    idmodelo = models.AutoField(db_column='idModelo', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'categoria'
        verbose_name_plural='Categoria' 


    def __str__(self):
        return self.nombre


from datetime import datetime, timedelta

datenow = datetime.now()

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
    horainicio = models.TimeField(db_column='Hora inicio',default=None)  # Field name made lowercase.
    horafin=models.TimeField(db_column='Hora fin',default=None)
    tipocontrato = models.ForeignKey('Tipocontrato', models.DO_NOTHING, db_column='Tipocontrato',default=1)  # Field name made lowercase.
    user=models.ForeignKey(User,db_column='Arrendatario', on_delete=models.CASCADE,related_name='bicicleta',null=True)
    bicicleta = models.ForeignKey(MiBicicleta, models.DO_NOTHING, db_column='Bicicleta',null=True)  # Field name made lowercase.
    estado = models.BooleanField(db_column='estado',default=True)


    class Meta:
        verbose_name_plural='Contratos'
    
    def get_absolute_url(self):
        return reverse('home', args=[self.id])




class FotoPerfiluser(models.Model):
    idfotouser = models.AutoField(db_column='idfotoUser', primary_key=True)  # Field name made lowercase.
    foto = models.CharField(max_length=100)
    usuario_idusuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='Usuario_idUsuario')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'foto_perfiluser'
        verbose_name_plural='Foto perfil Usuario'


class Materialbicicletas(models.Model):
    idmaterialbicicletas = models.AutoField(db_column='idMaterialBicicletas', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'materialbicicletas'
        verbose_name_plural='Material Bicicletas'

    def __str__(self):
        return self.nombre




class Pagos(models.Model):
    idpago = models.AutoField(db_column='idPago', primary_key=True)  # Field name made lowercase.
    fechapago = models.DateTimeField(db_column='FechaPago')  # Field name made lowercase.
    totalalquiler = models.DecimalField(db_column='TotalAlquiler', max_digits=6, decimal_places=3)  # Field name made lowercase.
    fechamora = models.DateTimeField(db_column='FechaMora', blank=True, null=True)  # Field name made lowercase.
    contrato = models.ForeignKey(ContratoBicicleta, models.DO_NOTHING, db_column='contrato')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Pagos'
        verbose_name_plural='Pagos'


class Perfilusuario(models.Model):
    idroles = models.AutoField(db_column='idRoles', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=45)  # Field name made lowercase.
    descripcionrol = models.TextField(db_column='descripcionRol', blank=True, null=True)  # Field name made lowercase.
    usuario_idusuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='Usuario_idUsuario')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'perfilusuario'
        verbose_name_plural='Perfil Usuario' 


class Persona(models.Model):
    idpersona = models.AutoField(db_column='idPersona', primary_key=True)  # Field name made lowercase.
    nombres = models.CharField(db_column='Nombres', max_length=50)  # Field name made lowercase.
    apellidos = models.CharField(db_column='Apellidos', max_length=50)  # Field name made lowercase.
    numidentificacion = models.BigIntegerField(db_column='NumIdentificacion')  # Field name made lowercase.
    numcelular = models.BigIntegerField(db_column='NumCelular')  # Field name made lowercase.
    numtelefono = models.BigIntegerField(db_column='NumTelefono', blank=True, null=True)  # Field name made lowercase.
    correoelectronico = models.CharField(db_column='CorreoElectronico', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'persona'
        verbose_name_plural='Persona' 


    def __str__(self):
        cadenaName = self.nombres + ' ' + self.apellidos
        return cadenaName



class Privilegios(models.Model):
    idprivilegios = models.AutoField(db_column='idPrivilegios', primary_key=True)  # Field name made lowercase.
    privilegio = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'privilegios'


class Reserva(models.Model):
    idreserva = models.AutoField(db_column='idReserva', primary_key=True)  # Field name made lowercase.
    bicicleta = models.ForeignKey(MiBicicleta, models.DO_NOTHING, db_column='Bicicleta')  # Field name made lowercase.
    disponibleen = models.TimeField(db_column='DisponibleEn', blank=True, null=True)  # Field name made lowercase.
    disponible = models.CharField(db_column='Disponible', max_length=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'reserva'
        verbose_name_plural='Reserva' 


class Tiempoprestamo(models.Model):
    idtiempodisponibilidad = models.IntegerField(db_column='idTiempoDisponibilidad', primary_key=True)  # Field name made lowercase.
    bicicletas_idbicicletas = models.ForeignKey(MiBicicleta, models.DO_NOTHING, db_column='Bicicletas_idBicicletas')  # Field name made lowercase.
    contrato_idcontrato = models.ForeignKey(ContratoBicicleta, models.DO_NOTHING, db_column='Contrato_idContrato')  # Field name made lowercase.
    tiempoinicio = models.CharField(db_column='tiempoInicio', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tiempoprestamo'
        verbose_name_plural='Tiempo Prestamo'


class Tipocontrato(models.Model):
    idtipocontrato = models.AutoField(db_column='idtipocontrato', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=45)  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'tipocontrato'
        verbose_name_plural='Tipo contrato'
        managed = False

    def __str__(self):
        return self.nombre 

class Usuario(models.Model):
    idusuario = models.AutoField(db_column='idUsuario', primary_key=True)  # Field name made lowercase.
    usuario = models.CharField(db_column='Usuario', max_length=20)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=100)  # Field name made lowercase.
    persona_idpersona = models.ForeignKey(Persona, models.DO_NOTHING, db_column='Persona_idPersona')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'usuario'


class CatalogoBicicleta(models.Model):
    bicicleta = models.JSONField()  # Field name made lowercase.
    name=models.CharField(db_column='Nombre',max_length=50)

    class Meta:
        verbose_name_plural='Catalogo'


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
        verbose_name_plural = 'Contacto'