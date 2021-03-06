# Generated by Django 3.2.5 on 2022-01-20 22:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecgsproject', '0019_auto_20220120_2335'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultat',
            name='result',
            field=models.FloatField(blank=True, default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contrat',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ecgsproject.client'),
        ),
    ]
