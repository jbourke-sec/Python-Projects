# Generated by Django 3.2.9 on 2022-03-08 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vulnApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='policy',
            name='category',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='policy',
            name='cpe',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]