# Generated by Django 3.2.5 on 2022-01-26 17:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecgsproject', '0031_auto_20220125_2346'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name_plural': 'Données personnelles'},
        ),
        migrations.AlterModelOptions(
            name='employe',
            options={'verbose_name_plural': 'Vendeurs'},
        ),
    ]
