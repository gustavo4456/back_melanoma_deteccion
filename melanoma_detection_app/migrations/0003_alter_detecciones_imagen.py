# Generated by Django 4.2.4 on 2023-09-12 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('melanoma_detection_app', '0002_remove_usuarios_imagen_usuarios_foto_perfil'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detecciones',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='detections/'),
        ),
    ]
