# Generated by Django 2.2.6 on 2022-03-29 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0002_auto_20220328_2327'),
    ]

    operations = [
        migrations.AddField(
            model_name='busqueda',
            name='url',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
