from django.contrib import admin
from .models import * # Se  importan todas las tablas del modelo de base de datos del archivo models.py 
from Apps.usuario.models import User # Se trae el modelo usario personalizado

from import_export import resources
from import_export.admin import ImportExportActionModelAdmin, ImportExportModelAdmin



admin.site.site_header="Administración Biken"
admin.site.site_title="Biken"



class UserResources(resources.ModelResource):
    class Meta:
        model = User


@admin.register (User)
class userAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('username','first_name','last_name','numcelular','email','is_staff','is_active')
    search_fields = ['last_name','first_name']
    list_editable = ['is_active']
    list_filter = ['is_active']
    list_per_page = 10
    resource_class = UserResources 

    pass

class BicicletaResources(resources.ModelResource):
    class Meta:
        model = MiBicicleta

@admin.register (MiBicicleta)
class BicletasAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('user','idmibicicleta','marca','color', 'material', 'categoria','precioalquiler','timestamp','foto','valortiempohoras','valortiempomin','disponible')
    search_fields = ['user__first_name__icontains','idmibicicleta','marca', 'material__nombre__icontains', 'categoria__nombre__icontains','precioalquiler','timestamp','valortiempohoras','disponible']
    list_editable = ['precioalquiler','valortiempohoras']
    list_filter = ['marca','categoria','material','disponible']
    list_per_page = 10
    resource_class = BicicletaResources

    pass

@admin.register (Pagos)
class PagosAdmin(admin.ModelAdmin):
    list_display =  ('idpago','fechapago','totalalquiler','fechamora','contrato')
    search_fields = ['contrato']
    list_filter = ['contrato','fechapago']
    list_per_page = 10
    pass



@admin.register (Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ['nombre']
    # list_editable = ['nombre']
    list_filter = ['nombre']
    list_per_page = 10
    pass

@admin.register (Materialbicicletas)
class MaterialbicicletasAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ['nombre']
    # list_editable = ['nombre']
    list_filter = ['nombre']
    list_per_page = 10
    pass



@admin.register (ContratoBicicleta)
class ContratoAdmin(admin.ModelAdmin):
    list_display = ('id','fechainicio', 'fechafin','tipodocumento','numerodocumento','direccion','horainicio','horafin','tipocontrato','user','bicicleta')
    search_fields = ['fechainicio','fechafin']
    # list_editable = ['fechainicio']
    list_filter = ['fechainicio','fechafin']
    list_per_page = 10
    pass





@admin.register (Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('disponibleen','disponible')
    # search_fields = ['disponibleen']
    list_editable = ['disponible']
    # list_filter = ['disponibleen']
    list_per_page = 10
    pass



@admin.register (Tipocontrato)
class TipocontratoAdmin(admin.ModelAdmin):
    list_display = ('nombre','descripcion')
    search_fields = ['nombre']
    # list_editable = ['nombre']
    list_filter = ['nombre']
    list_per_page = 10
    pass


@admin.register(Tiempoprestamo)
class TiempoprestamoAdmin(admin.ModelAdmin):
    list_display = ('idtiempodisponibilidad','bicicletas_idbicicletas','contrato_idcontrato','tiempoinicio')
    search_fields = ['idtiempodisponibilidad']
    # list_editable = ['tiempoinicio']
    list_filter = ['tiempoinicio']
    list_per_page = 10

    pass


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display=('id','name','asunto','email','mensaje')