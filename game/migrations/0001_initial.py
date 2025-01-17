# Generated by Django 3.2.25 on 2024-09-06 20:35

import django.core.validators
from django.db import migrations, models
import game.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False, validators=[django.core.validators.MinLengthValidator(5, 'El ID debe ser de al menos 5 caracteres')])),
                ('title', models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(1, 'El titulo no puede estar vacio')])),
                ('desc', models.CharField(max_length=5000)),
                ('icon', models.ImageField(upload_to=game.models.game_icon_dir_path)),
                ('release_date', models.DateField(blank=True, null=True)),
            ],
        ),
    ]
