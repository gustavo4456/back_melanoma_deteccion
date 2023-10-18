from django.contrib import admin
from .models import Notificaciones


# Register your models here.
@admin.register(Notificaciones)
class NotificacionesAdmin(admin.ModelAdmin):
    list_display = ['id', 'mensaje', 'fecha']
    search_fields = ['mensaje']
    list_filter = ['fecha']