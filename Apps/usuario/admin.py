from django.contrib import admin

#Register your models here.
from Apps.principal.models import Perfil



@admin.register(Perfil)
class TiempoprestamoAdmin(admin.ModelAdmin):
    list_display = ('user','telefono','direccion','estado')
    search_fields=['user','direccion']
    list_filter=['user','direccion']
    list_per_page=10

    pass


