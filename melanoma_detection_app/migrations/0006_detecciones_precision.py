# Generated by Django 4.2.4 on 2023-10-02 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('melanoma_detection_app', '0005_alter_usuariosdetecciones_es_favorito'),
    ]

    operations = [
        migrations.AddField(
            model_name='detecciones',
            name='precision',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
