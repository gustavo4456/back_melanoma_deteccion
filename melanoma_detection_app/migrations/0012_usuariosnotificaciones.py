# Generated by Django 4.2.4 on 2023-10-22 19:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('melanoma_detection_app', '0011_alter_usuarios_fecha_nacimiento'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsuariosNotificaciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leido', models.BooleanField(default=False)),
                ('notificacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='melanoma_detection_app.notificaciones')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
