# Generated by Django 3.1.2 on 2020-12-13 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contentUploaderApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='convertedFilePaths',
            field=models.CharField(max_length=500),
        ),
    ]
