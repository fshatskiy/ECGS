# Generated by Django 3.2.5 on 2021-09-02 18:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecgsproject', '0002_customuser_createur'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employe',
            name='id_integrateur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ecgsproject.integrateur'),
        ),
    ]
