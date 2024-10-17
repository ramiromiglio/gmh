from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import *
from user.models import *
import zipfile
import io

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

class ModForm(forms.ModelForm):
    files = MultipleFileField()
    images = MultipleFileField()
    desc = forms.CharField(max_length=5000, widget=forms.Textarea)

    class Meta:
        model = Mod
        fields = (
            'related_game',
            'title',
            'short_desc',
            'version',
            'icon',
            'desc',
            'youtube_link',
            'category',
        )