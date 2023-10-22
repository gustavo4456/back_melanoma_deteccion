from django.contrib import admin
from .models import Notificaciones, UsuariosNotificaciones

# Register your models here.

@admin.register(UsuariosNotificaciones)
class UsuariosNotificacionesAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'notificacion', 'leido']
    list_filter = ['leido']
    search_fields = ['usuario__username', 'notificacion__mensaje']

@admin.register(Notificaciones)
class NotificacionesAdmin(admin.ModelAdmin):
    list_display = ['id', 'mensaje', 'fecha']
    search_fields = ['mensaje']
    list_filter = ['fecha']