from rest_framework import serializers
from .models import Usuarios, Etiquetas, UsuariosDetecciones, Detecciones, ConfiguracionUsuario, Notificaciones

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        fields = '__all__'

class EtiquetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etiquetas
        fields = '__all__'

class DeteccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detecciones
        fields = '__all__'

class UsuariosDeteccionesSerializer(serializers.ModelSerializer):
    # deteccion = DeteccionSerializer()
    class Meta:
        model = UsuariosDetecciones
        fields = '__all__'  # Esto serializará todos los campos del modelo UsuariosDetecciones
        depth = 1  # Asegura que se incluyan los datos completos de las relaciones

class ConfiguracionUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracionUsuario
        fields = '__all__'

class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificaciones
        fields = '__all__'