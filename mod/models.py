from typing import Iterable
from django.db import models
from django.urls import reverse
from django.core.validators import MinLengthValidator, RegexValidator, FileExtensionValidator, MinValueValidator, MaxValueValidator
from django.core.files.base import ContentFile
from user.models import User
from game.models import Game
import re
from django.core.exceptions import ValidationError
import datetime
import zipfile
import io
from PIL import Image
import os
import uuid
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import *

class ModPath:
    def _sanitize_extentsion(ext: str):
        return re.sub('[^a-zA-Z0-9]', '', ext)

    def _sanitize_filename(filename: str):
        ext = None
        ext_len = 0
        sep = filename.rfind('.')
        if sep != -1:
            ext = filename[sep + 1:]
            ext = ModPath._sanitize_extentsion(ext)
            filename = filename[:sep]
        if ext is not None:
            ext_len = len(ext) + 1
        
        length = len(filename) + ext_len
        if length > 255:
            filename = filename[:255-ext_len]
        filename = re.sub('[^a-zA-Z0-9]', '-', filename)
        if ext is not None:
            filename += ('.' + ext)
        return filename

    def icon(instance, filename):
        return f'games/{instance.related_game.id}/icon.jpg'

    def image(instance, filename):
        game_id = instance.related_mod.related_game.id
        mod_pk  = instance.related_mod.pk
        return f'games/{game_id}/mods/{mod_pk}/images/{ModPath._sanitize_filename(filename)}'

    def content(instance, filename):
        game_id = instance.related_mod.related_game.id
        mod_pk  = instance.related_mod.pk
        return f'games/{game_id}/mods/{mod_pk}/files/{ModPath._sanitize_filename(filename)}'

class ModCategory(models.Model):
    name = models.CharField(max_length=32)
    
    def __str__(self):
        return self.name

class Mod(models.Model):    
    title           = models.CharField(max_length=255, verbose_name='Nombre del mod')
    short_desc      = models.CharField(max_length=5000, verbose_name='Resumen del mod de unas pocas lineas', blank=True)
    desc            = models.CharField(max_length=5000, verbose_name='Descripcion')
    version         = models.IntegerField(validators=[MinValueValidator(1)], verbose_name='Version')
    author          = models.ForeignKey(User, on_delete=models.PROTECT)
    related_game    = models.ForeignKey(Game, on_delete=models.PROTECT, verbose_name='Juego base')
    icon            = ProcessedImageField(upload_to=ModPath.icon,
                                          processors=[Resize(340, 240)],
                                          format='JPEG',
                                          options={'quality': 100})
    data_size       = models.BigIntegerField()
    upload_date     = models.DateTimeField(auto_now_add=True)
    downloads_count = models.BigIntegerField(default=0)
    youtube_link    = models.URLField(null=True, blank=True)
    category        = models.ManyToManyField(ModCategory)
    ratings_sum     = models.IntegerField(verbose_name='Suma de todas las valoraciones (van de 1 a 5)', default=0)
    ratings_count   = models.IntegerField(verbose_name='Conteo de valoraciones unicas por usuario', default=0)

    def get_absolute_url(self):
        return reverse('mod-detail', args=[str(self.pk)])

    def get_some_categories(self):
        return self.category.values_list('name', flat=True)[:3]
    
    def calc_rating(self):
        self.ratings_sum / self.ratings_count

    def __str__(self):
        return self.title

class ModImage(models.Model):
    related_mod  = models.ForeignKey(Mod, on_delete=models.CASCADE)
    image        = ProcessedImageField(upload_to=ModPath.image,
                                       processors=[Resize(1280, 720)],
                                       format='JPEG',
                                       options={'quality': 100})
    
    def __str__(self):
        file_name = self.image.name.split('/')[-1]
        return f'Image [{file_name}]'

class ModFile(models.Model):
    related_mod        = models.ForeignKey(Mod, on_delete=models.CASCADE)
    file               = models.FileField(upload_to=ModPath.content)
    original_file_name = models.CharField(max_length=255)