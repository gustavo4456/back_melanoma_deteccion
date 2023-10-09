from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

class Usuarios(AbstractUser):
    fecha_nacimiento = models.DateField()
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
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    mensaje = models.CharField(max_length=2048)
    fecha = models.DateTimeField()

    def __str__(self):
        return f"Notificación {self.id}"

class UsuariosDetecciones(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    deteccion = models.ForeignKey(Detecciones, on_delete=models.CASCADE)
    etiqueta = models.ForeignKey(Etiquetas, on_delete=models.CASCADE)
    es_favorito = models.BooleanField(default = False)

    def __str__(self):
        return f"Usuario: {self.usuario}, Detección: {self.deteccion}"
