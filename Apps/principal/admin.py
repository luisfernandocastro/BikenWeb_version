from django.contrib import admin
from .models import * # Se  importan todas las tablas del modelo de base de datos del archivo models.py 
from Apps.usuario.models import User # Se trae el modelo usario personalizado


admin.site.site_header="Administración Biken"
admin.site.site_title="Biken"

@admin.register (User)
class userAdmin(admin.ModelAdmin):
    list_display = ('username','first_name','last_name','numcelular','email','is_staff','is_active')
    search_fields = ['username','is_staff']
    list_filter = ['username','first_name','last_name','is_staff']
    list_per_page = 10

    pass



@admin.register (MiBicicleta)
class BicletasAdmin(admin.ModelAdmin):
    list_display = ('user','idmibicicleta','marca','color', 'material', 'categoria','precioalquiler','timestamp','foto','valortiempohoras','valortiempomin','disponible')
    search_fields = ['color']
    list_editable = ['precioalquiler','valortiempohoras']
    list_filter = ['color','categoria']
    list_per_page = 10

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



@admin.register (Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = ('cantidadbicicletas','fechainicio', 'fechafin', 'tiempo', 'observaciones','tipocontrato','persona_idpersona','bicicletas_idbicicletas')
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
    list_display = ('idtipocontrato','nombre','descripcion')
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






