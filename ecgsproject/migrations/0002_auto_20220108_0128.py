# Generated by Django 3.2.5 on 2022-01-08 00:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecgsproject', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contrat',
            name='contrat_detail',
        ),
        migrations.AddField(
            model_name='contrat_detail',
            name='contrat',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='ecgsproject.contrat'),
            preserve_default=False,
        ),
    ]
