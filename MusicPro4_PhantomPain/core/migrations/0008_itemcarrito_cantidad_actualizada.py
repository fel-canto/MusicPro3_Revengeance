# Generated by Django 4.2.1 on 2023-06-04 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_carrito_itemcarrito'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemcarrito',
            name='cantidad_actualizada',
            field=models.PositiveIntegerField(default=0),
        ),
    ]