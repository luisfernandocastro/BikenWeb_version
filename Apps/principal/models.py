# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from BikenPro.settings import MEDIA_URL, STATIC_URL
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator,MinLengthValidator
from django.utils import timezone
User=get_user_model()


    
class Perfil(models.Model):
    user=  models.OneToOneField(User,on_delete=models.CASCADE)
    telefono = models.BigIntegerField(db_column='Telefono',null=True,blank=True, validators=[MinLengthValidator(7)])
    direccion = models.CharField(db_column='Direccion', max_length=50,null=True,blank=True)
    biografia = models.TextField(db_column='Biografia', max_length=150,null=True,blank=True) 
    image_portada = models.ImageField(upload_to='user/banner/%Y/%m/%d',null=True,blank=True,verbose_name='Imagen de portada')
    image_user = models.ImageField(upload_to='user/%Y/%m/%d',null=True,blank=True,verbose_name='Imagen de perfil')

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



class MiBicicleta(models.Model):
    idmibicicleta = models.BigAutoField(db_column='idmibicicleta',primary_key=True, serialize=False, verbose_name='ID')
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='miBici',null=True)
    marca = models.CharField(db_column='Marca', max_length=45,default=None)  # Field name made lowercase.
    color = models.CharField(db_column='Color', max_length=50,default=None)  # Field name made lowercase.
    material = models.ForeignKey('Materialbicicletas', models.DO_NOTHING, db_column='Material',default=None)  # Field name made lowercase.
    timestamp=models.DateTimeField(db_column='Fecha de subida',default=timezone.now)
    categoria = models.ForeignKey('Categoria', models.DO_NOTHING, db_column='Categoria',default=None)  # Field name made lowercase.
    precioalquiler = models.DecimalField(db_column='PrecioAlquiler', max_digits=6, decimal_places=3,verbose_name='Precio Alquiler',default=None)  # Field name made lowercase.
    valortiempohoras= models.IntegerField(db_column='Horas de alquiler',null=True,blank=True,default=0)
    valortiempomin= models.IntegerField(db_column='Minutos de alquiler',null=True,blank=True,default=0)
    descripcionbici = models.TextField(db_column='DescripcionBici', max_length=150,null=True,default=None,blank=True) 
    foto = models.ImageField(db_column='Foto', max_length=100, null=True)  # Field name made lowercase.

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


class Contrato(models.Model):
    idcontrato = models.AutoField(db_column='idContrato', primary_key=True)  # Field name made lowercase.
    cantidadbicicletas = models.IntegerField(db_column='CantidadBicicletas')  # Field name made lowercase.
    fechainicio = models.DateField(db_column='FechaInicio')  # Field name made lowercase.
    fechafin = models.DateField(db_column='FechaFin')  # Field name made lowercase.
    tiempo = models.TimeField(db_column='Tiempo')  # Field name made lowercase.
    observaciones = models.CharField(db_column='Observaciones', max_length=100)  # Field name made lowercase.
    tipocontrato = models.ForeignKey('Tipocontrato', models.DO_NOTHING, db_column='Tipocontrato')  # Field name made lowercase.
    persona_idpersona = models.ForeignKey('Persona', models.DO_NOTHING, db_column='Persona_idPersona')  # Field name made lowercase.
    bicicletas_idbicicletas = models.ForeignKey(MiBicicleta, models.DO_NOTHING, db_column='Bicicletas_idBicicletas')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Contrato'
        verbose_name_plural='Contratos'


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
    contrato = models.ForeignKey(Contrato, models.DO_NOTHING, db_column='Tipo de Contrato')  # Field name made lowercase.

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
    contrato_idcontrato = models.ForeignKey(Contrato, models.DO_NOTHING, db_column='Contrato_idContrato')  # Field name made lowercase.
    tiempoinicio = models.CharField(db_column='tiempoInicio', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tiempoprestamo'
        verbose_name_plural='Tiempo Prestamo'


class Tipocontrato(models.Model):
    idtipocontrato = models.IntegerField(db_column='idTipocontrato', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=45)  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tipocontrato'


class Usuario(models.Model):
    idusuario = models.AutoField(db_column='idUsuario', primary_key=True)  # Field name made lowercase.
    usuario = models.CharField(db_column='Usuario', max_length=20)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=100)  # Field name made lowercase.
    persona_idpersona = models.ForeignKey(Persona, models.DO_NOTHING, db_column='Persona_idPersona')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'usuario'
