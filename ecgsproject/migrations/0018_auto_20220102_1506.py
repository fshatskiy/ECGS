# Generated by Django 3.2.5 on 2022-01-02 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecgsproject', '0017_auto_20220101_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='modified_by',
            field=models.CharField(blank=True, editable=False, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='contrat',
            name='modified_by',
            field=models.CharField(blank=True, editable=False, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='contrat',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='modified_by',
            field=models.CharField(blank=True, editable=False, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='employe',
            name='modified_by',
            field=models.CharField(blank=True, editable=False, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='employe',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='integrateur',
            name='modified_by',
            field=models.CharField(blank=True, editable=False, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='integrateur',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
