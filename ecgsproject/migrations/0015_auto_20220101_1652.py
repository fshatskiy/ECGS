# Generated by Django 3.2.5 on 2022-01-01 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecgsproject', '0014_auto_20211230_1518'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='created_by',
            field=models.CharField(default=1, max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='modified_by',
            field=models.CharField(default=2, max_length=254),
            preserve_default=False,
        ),
    ]
