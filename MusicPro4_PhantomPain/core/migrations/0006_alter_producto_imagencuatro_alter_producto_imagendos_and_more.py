# Generated by Django 4.2.1 on 2023-06-01 01:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_producto_imagencuatro_alter_producto_imagendos_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='imagenCuatro',
            field=models.ImageField(null=True, upload_to='CarpetaDestino', verbose_name='Cuarta imagen'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='imagenDos',
            field=models.ImageField(null=True, upload_to='CarpetaDestino', verbose_name='Segunda imagen'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='imagenTres',
            field=models.ImageField(null=True, upload_to='CarpetaDestino', verbose_name='Tercera imagen'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='tipoNombre',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='core.tipoproducto', verbose_name='La llave del tipo de producto'),
        ),
    ]
