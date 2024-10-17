from typing import Iterable
from django.db import models
from django.urls import reverse
from django.core.validators import MinLengthValidator, RegexValidator, FileExtensionValidator, MinValueValidator
from django.core.files.base import ContentFile
from user.models import User
import re
from django.core.exceptions import ValidationError
import datetime
import io
from PIL import Image
from imagekit.models import ProcessedImageField
from imagekit.processors import *

def game_icon_dir_path(instance, filename):
    return f'games/{instance.id}/ico.jpg'

def mb(n):
    return 1024 * 1024 * n

def convert_fieldimage_format_to_webp_and_apply(imagefield):
    image = Image.open(imagefield)
    buf = io.BytesIO()
    image.save(buf, format="WebP")
    imagefield.save(imagefield.name, ContentFile(buf.getvalue()), save=False)
    print(imagefield.name + " converted to webp")


class Game(models.Model):
    
    id           = models.CharField(primary_key=True, max_length=32, validators=[MinLengthValidator(5, "El ID debe ser de al menos 5 caracteres")])
    title        = models.CharField(max_length=255, validators=[MinLengthValidator(1, "El titulo no puede estar vacio")])
    desc         = models.CharField(max_length=5000)
    icon         = ProcessedImageField(upload_to=game_icon_dir_path,
                                       processors=[Resize(648, 800)],
                                       format='JPEG',
                                       options={'quality': 100})
    release_date = models.DateField(blank=True, null=True)

    def clean(self):
        # Id
        if self.id and not re.compile(r'^[a-z](?:(?:-[a-z0-9])*[a-z0-9]*)*$').match(self.id):
            raise ValidationError({"id": "El ID no es valido" })
        # Icon
        if self.icon and self.icon.size > mb(8):
            raise ValidationError({"icon": "El icono debe ser menor a 8mb"})
        # Release Date
        if self.release_date and self.release_date >= datetime.date.today():
            raise ValidationError({"release_date": "La fecha de publicacion debe ser mas antigua"})  
        super().clean()

    def get_absolute_url(self):
        return reverse('game-detail', args=[str(self.id)])
    
    def short_desc(self):
        return self.desc[:100] + '...'

    def __str__(self):
        return self.title