# Generated by Django 3.2.5 on 2022-01-20 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecgsproject', '0013_auto_20220120_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrat',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ecgsproject.client'),
        ),
        migrations.AlterField(
            model_name='contrat_detail',
            name='contrat',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ecgsproject.contrat'),
        ),
        migrations.AlterField(
            model_name='licence',
            name='contrat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ecgsproject.contrat'),
        ),
    ]
