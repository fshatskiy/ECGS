# Generated by Django 3.2.5 on 2022-01-20 15:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecgsproject', '0012_alter_contrat_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrat',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecgsproject.client'),
        ),
        migrations.AlterField(
            model_name='contrat_detail',
            name='contrat',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='ecgsproject.contrat'),
        ),
        migrations.AlterField(
            model_name='licence',
            name='contrat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ecgsproject.contrat'),
        ),
    ]