# Generated by Django 3.2.5 on 2021-12-30 13:31

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ecgsproject', '0012_contrat_num_contrat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contrat_detail',
            name='contrat_ptr',
        ),
        migrations.AddField(
            model_name='contrat_detail',
            name='contrat',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ecgsproject.contrat'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contrat_detail',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contrat_detail',
            name='modified_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
