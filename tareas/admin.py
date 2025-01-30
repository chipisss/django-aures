from django.contrib import admin
from .models import Tarea


class TareaAdmin(admin.ModelAdmin):
    readonly_fields=('creado',)
# Register your models here.
admin.site.register(Tarea,TareaAdmin)