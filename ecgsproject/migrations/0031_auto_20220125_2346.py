# Generated by Django 3.2.5 on 2022-01-25 22:46

from django.db import migrations
import vies.models


class Migration(migrations.Migration):

    dependencies = [
        ('ecgsproject', '0030_auto_20220124_1947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='tva_cli',
            field=vies.models.VATINField(max_length=14, unique=True, verbose_name='tva'),
        ),
        migrations.AlterField(
            model_name='integrateur',
            name='tva_integrateur',
            field=vies.models.VATINField(max_length=14, unique=True, verbose_name='tva'),
        ),
    ]
