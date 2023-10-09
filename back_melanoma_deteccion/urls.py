from django.contrib import admin
from django.urls import path
from saludos import views as saludos_views
from melanoma import views as melanoma_views
from melanoma_detection_app import views as viewsDB

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('suma/<int:num1>/<int:num2>/', saludos_views.suma, name='suma'),
    path('api/hola-mundo/', saludos_views.hola_mundo, name='hola_mundo'),
    path('api/detect-melanoma/', melanoma_views.detect_melanoma, name='detect_melanoma'),

    path('api/usuarios/', viewsDB.get_usuarios, name='usuario-list'),
    path('api/usuarios/registro/', viewsDB.registrar_usuario, name='registro_usuario'),
    path('api/usuarios/<int:pk>/', viewsDB.update_usuario, name='update_usuario'),

    path('api/etiquetas/', viewsDB.get_etiquetas, name='etiquetas-list'),
    path('api/detecciones-usuarios/', viewsDB.get_detecciones, name='deteccion-usuarios-list'),
    path('api/delete-detecciones-usuarios/', viewsDB.delete_usuarios_detecciones, name='delete_usuarios_detecciones'),




path('api/configuracion-usuario/', viewsDB.configuracion_usuario, name='configuracion_usuario'),




    path('api/login/', viewsDB.user_login, name='user_login'),
    path('api/logout/', viewsDB.user_logout, name='user_logout'),
    path('api/check-authentication/', viewsDB.check_authentication, name='check_authentication'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
