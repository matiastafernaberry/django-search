# Generated by Django 2.2.6 on 2022-04-20 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0008_auto_20220419_1831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultadobusqueda',
            name='fecha_modificacion',
            field=models.DateTimeField(verbose_name='fecha modificacion'),
        ),
    ]