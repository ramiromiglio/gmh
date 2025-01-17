# Generated by Django 3.2.25 on 2024-09-06 20:35

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields
import mod.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Nombre del mod')),
                ('short_desc', models.CharField(max_length=5000, verbose_name='Resumen del mod de unas pocas lineas')),
                ('desc', models.CharField(max_length=5000, verbose_name='Descripcion')),
                ('version', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Version')),
                ('icon', imagekit.models.fields.ProcessedImageField(upload_to=mod.models.ModPath.icon)),
                ('data_size', models.BigIntegerField()),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('downloads_count', models.BigIntegerField(default=0)),
                ('youtube_link', models.URLField(null=True)),
                ('ratings_sum', models.IntegerField(default=0, verbose_name='Suma de todas las valoraciones (van de 1 a 5)')),
                ('ratings_count', models.IntegerField(default=0, verbose_name='Conteo de valoraciones unicas por usuario')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ModCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='ModImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to=mod.models.ModPath.image)),
                ('related_mod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mod.mod')),
            ],
        ),
        migrations.CreateModel(
            name='ModFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=mod.models.ModPath.content)),
                ('original_file_name', models.CharField(max_length=255)),
                ('related_mod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mod.mod')),
            ],
        ),
        migrations.AddField(
            model_name='mod',
            name='category',
            field=models.ManyToManyField(to='mod.ModCategory'),
        ),
        migrations.AddField(
            model_name='mod',
            name='related_game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='game.game', verbose_name='Juego base'),
        ),
    ]
