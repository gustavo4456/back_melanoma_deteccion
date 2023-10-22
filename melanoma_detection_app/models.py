from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from datetime import datetime

class Usuarios(AbstractUser):
    fecha_nacimiento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=50)
    foto_perfil = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class ConfiguracionUsuario(models.Model):
    usuario = models.OneToOneField(Usuarios, on_delete=models.CASCADE, unique=True)
    notificaciones_habilitadas = models.BooleanField(default= True)
    tema_preferido = models.BooleanField(default = False)

    def __str__(self):
        return f"Configuración de {self.usuario}"

class Detecciones(models.Model):
    imagen = models.ImageField(upload_to='detections/', null=True, blank=True)
    fecha_creacion = models.DateTimeField(default=datetime.now)
    resultado = models.CharField(max_length=2048)
    precision = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Detección {self.id}"

class Etiquetas(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Notificaciones(models.Model):
    mensaje = models.CharField(max_length=2048)
    fecha = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"Notificación {self.id}"

class UsuariosDetecciones(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    deteccion = models.ForeignKey(Detecciones, on_delete=models.CASCADE)
    etiqueta = models.ForeignKey(Etiquetas, on_delete=models.CASCADE)
    es_favorito = models.BooleanField(default = False)

    def __str__(self):
        return f"Usuario: {self.usuario}, Detección: {self.deteccion}"
    

class UsuariosNotificaciones(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    notificacion = models.ForeignKey(Notificaciones, on_delete=models.CASCADE)
    leido = models.BooleanField(default=False)  # Campo para rastrear si la notificación fue leída o no

    def __str__(self):
        return f"Usuario: {self.usuario}, Notificación: {self.notificacion}"




# Define el manejador de señales
@receiver(post_save, sender=Notificaciones)
def create_usuarios_notificaciones(sender, instance, created, **kwargs):
    if created:
        from .models import UsuariosNotificaciones  # Importa tu modelo de UsuariosNotificaciones aquí

        # Obtén todos los usuarios
        users = Usuarios.objects.all()

        # Crea un registro en UsuariosNotificaciones para cada usuario
        for user in users:
            UsuariosNotificaciones.objects.create(usuario=user, notificacion=instance, leido=False)
