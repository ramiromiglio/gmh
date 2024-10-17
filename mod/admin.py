from django.contrib import admin
from .models import Mod, ModImage, ModCategory
from .forms import ModForm

class ModAdmin(admin.ModelAdmin):
    pass

admin.site.register(Mod, ModAdmin)
admin.site.register(ModImage)
admin.site.register(ModCategory)