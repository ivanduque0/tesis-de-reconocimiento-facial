# Generated by Django 4.0.2 on 2022-03-03 19:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crudpostgres', '0002_rename_interaccion_interacciones'),
    ]

    operations = [
        migrations.CreateModel(
            name='oficina',
            fields=[
                ('nombre', models.CharField(max_length=50)),
                ('cedula', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.AddField(
            model_name='interacciones',
            name='cedula',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='cedulas', to='crudpostgres.oficina'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='interacciones',
            name='nombre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='nombres', to='crudpostgres.oficina'),
        ),
    ]
