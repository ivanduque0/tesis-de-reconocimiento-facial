# Generated by Django 4.0.2 on 2022-03-02 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pruebadb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='fundacion',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]