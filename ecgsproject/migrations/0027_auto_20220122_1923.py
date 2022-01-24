# Generated by Django 3.2.5 on 2022-01-22 18:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecgsproject', '0026_auto_20220121_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='employe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ecgsproject.employe'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='entreprise',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='fonction',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]