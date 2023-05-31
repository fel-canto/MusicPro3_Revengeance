# Generated by Django 4.2.1 on 2023-05-29 23:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreProducto', models.CharField(max_length=25, verbose_name='El nombre asociado al producto')),
                ('descripcionProducto', models.CharField(max_length=2000, verbose_name='La descripción asociada al producto en cuestión')),
                ('precioProducto', models.IntegerField(verbose_name='El precio asociado al producto')),
                ('stockProducto', models.IntegerField(verbose_name='El stock asociado al producto')),
                ('imagenUno', models.ImageField(upload_to='CarpetaDestino', verbose_name='Primera imagen')),
                ('imagenDos', models.ImageField(upload_to='CarpetaDestino', verbose_name='Segunda imagen')),
                ('imagenTres', models.ImageField(upload_to='CarpetaDestino', verbose_name='Tercera imagen')),
                ('imagenCuatro', models.ImageField(upload_to='CarpetaDestino', verbose_name='Cuarta imagen')),
            ],
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreRol', models.CharField(max_length=25, verbose_name='El nombre del rol de usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreUsuario', models.CharField(max_length=25, verbose_name='El nombre que el usuario usa para ingresar a su cuenta')),
                ('apellidos', models.CharField(max_length=25, verbose_name='El nombre que se mostrara algún día en la sección de comentarios')),
                ('correoUsuario', models.CharField(max_length=25, verbose_name='El correo asociado a la cuenta')),
                ('celular', models.IntegerField(verbose_name='El correo asociado a la cuenta')),
                ('clave', models.CharField(max_length=25, verbose_name='El correo asociado a la cuenta')),
                ('rol', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.rol', verbose_name='La llave de rol-usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaVenta', models.DateField()),
                ('totalVenta', models.IntegerField(verbose_name='El total asociado a la venta despues de el iva de mierda')),
                ('nombreUsuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.usuario', verbose_name='llave usuario-venta')),
            ],
        ),
        migrations.CreateModel(
            name='Detalle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('totalDetalle', models.IntegerField(verbose_name='El total asociado a la venta despues de el iva de mierda')),
                ('fechaVenta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.venta', verbose_name='llave Venta-Detalle')),
                ('nombreProducto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.producto', verbose_name='llave Venta-Detalle')),
            ],
        ),
    ]