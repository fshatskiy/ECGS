# Generated by Django 3.2.5 on 2022-01-01 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecgsproject', '0016_auto_20220101_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='created_by',
            field=models.CharField(editable=False, max_length=254),
        ),
        migrations.AlterField(
            model_name='client',
            name='modified_by',
            field=models.CharField(editable=False, max_length=254),
        ),
        migrations.AlterField(
            model_name='contrat',
            name='created_by',
            field=models.CharField(editable=False, max_length=254),
        ),
        migrations.AlterField(
            model_name='contrat',
            name='modified_by',
            field=models.CharField(editable=False, max_length=254),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='created_by',
            field=models.CharField(editable=False, max_length=254),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='modified_by',
            field=models.CharField(editable=False, max_length=254),
        ),
        migrations.AlterField(
            model_name='employe',
            name='created_by',
            field=models.CharField(editable=False, max_length=254),
        ),
        migrations.AlterField(
            model_name='employe',
            name='modified_by',
            field=models.CharField(editable=False, max_length=254),
        ),
        migrations.AlterField(
            model_name='integrateur',
            name='created_by',
            field=models.CharField(editable=False, max_length=254),
        ),
        migrations.AlterField(
            model_name='integrateur',
            name='modified_by',
            field=models.CharField(editable=False, max_length=254),
        ),
    ]