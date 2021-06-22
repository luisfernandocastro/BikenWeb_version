from django.contrib import admin
from .models import *
from Apps.usuario.models import User


admin.site.site_header="Administración Biken"
admin.site.site_title="Biken"

@admin.register (User)
class userAdmin(admin.ModelAdmin):
    list_display = ('username','first_name','last_name','email','is_staff')
    search_fields = ['username','is_staff']
    # list_editable = ['numcelular','correoelectronico']
    list_filter = ['username','first_name','is_staff']
    list_per_page = 10

    pass


@admin.register (Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('nombres','apellidos','numidentificacion','numcelular','numtelefono','correoelectronico',)
    search_fields = ['nombres','apellidos']
    list_editable = ['numcelular','correoelectronico']
    list_filter = ['nombres','correoelectronico']
    list_per_page = 10

    pass

@admin.register (MiBicicleta)
class BicletasAdmin(admin.ModelAdmin):
    list_display = ('idmibicicleta','marca','color', 'material', 'categoria','precioalquiler','foto')
    search_fields = ['color']
    list_editable = ['precioalquiler']
    list_filter = ['color','categoria']
    list_per_page = 10

    pass

@admin.register (Pagos)
class PagosAdmin(admin.ModelAdmin):
    # list_display =  ('nombres','apellidos','correoelectronico')
    # search_fields = ['nombres']
    # list_editable = ['apellidos']
    # list_filter = ['nombres','correoelectronico']
    # list_per_page = 10
    pass



@admin.register (Catalogo)
class CatalogoAdmin(admin.ModelAdmin):
    list_display = ('bicicleta','fechahorasubida')
    search_fields = ['bicicleta']
    # list_editable = ['fechahorasubida']
    list_filter = ['fechahorasubida']
    list_per_page = 2

    pass

@admin.register (Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ['nombre']
    # list_editable = ['nombre']
    list_filter = ['nombre']
    list_per_page = 2
    pass

@admin.register (Materialbicicletas)
class MaterialbicicletasAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ['nombre']
    # list_editable = ['nombre']
    list_filter = ['nombre']
    list_per_page = 2
    pass



@admin.register (Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = ('cantidadbicicletas','fechainicio', 'fechafin', 'tiempo', 'observaciones','tipocontrato','persona_idpersona','bicicletas_idbicicletas')
    search_fields = ['fechainicio','fechafin']
    # list_editable = ['fechainicio']
    list_filter = ['fechainicio','fechafin']
    list_per_page = 2
    pass

#@admin.register (Modulo)
#class ModuloAdmin(admin.ModelAdmin):
#    list_display = ('fechapago','totalalquiler','fechamora','contrato')
#    search_fields = ['fechapago']
#    # list_editable = ['fechapago',']
#    list_filter = ['fechapago']
#    list_per_page = 2
#    pass

@admin.register (Perfilusuario)
class PerfilusuarioAdmin(admin.ModelAdmin):
    # list_display =  ('nombres','apellidos','correoelectronico')
    # search_fields = ['nombres']
    # list_editable = ['apellidos']
    # list_filter = ['nombres','correoelectronico']
    # list_per_page = 10
    pass

#@admin.register (Privilegios)
#class PrivilegiosAdmin(admin.ModelAdmin):
    # list_display =  ('nombres','apellidos','correoelectronico')
    # search_fields = ['nombres']
    # list_editable = ['apellidos']
    # list_filter = ['nombres','correoelectronico']
    # list_per_page = 10

    #pass

@admin.register (Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('disponibleen','disponible')
    # search_fields = ['disponibleen']
    list_editable = ['disponible']
    # list_filter = ['disponibleen']
    list_per_page = 2
    pass

@admin.register (Tipocontrato)
class TipocontratoAdmin(admin.ModelAdmin):
    list_display = ('idtipocontrato','nombre','descripcion')
    search_fields = ['nombre']
    # list_editable = ['nombre']
    list_filter = ['nombre']
    list_per_page = 2
    pass


@admin.register(Tiempoprestamo)
class TiempoprestamoAdmin(admin.ModelAdmin):
    list_display = ('idtiempodisponibilidad','bicicletas_idbicicletas','contrato_idcontrato','tiempoinicio')
    search_fields = ['idtiempodisponibilidad']
    # list_editable = ['tiempoinicio']
    list_filter = ['tiempoinicio']
    list_per_page = 2

    pass

#@admin.register(Privilegios)
#class TiempoprestamoAdmin(admin.ModelAdmin):
#    list_display = ('idprivilegios','privilegio')
#    search_fields = ['privilegio']
#    list_editable = ['privilegio']
#    list_filter = ['privilegio']
#    list_per_page = 2

#    pass


@admin.register(Perfil)
class TiempoprestamoAdmin(admin.ModelAdmin):
    list_display = ('user',)
    pass





