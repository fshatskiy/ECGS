# Generated by Django 3.2.5 on 2022-01-20 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecgsproject', '0011_auto_20220117_1020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrat',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ecgsproject.client'),
        ),
    ]