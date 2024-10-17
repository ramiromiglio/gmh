from django.core.management.base import BaseCommand, CommandError
from game.models import Game
from mod.models import Mod, ModImage, ModCategory

class Command(BaseCommand):
    def handle(self, *args, **options):
        #if (Game.objects.all().count() > 0):
        #    raise CommandError('La tabla Game contiene instancias')
        if (Mod.objects.all().count() > 0):
            raise CommandError('La tabla Mod contiene instancias')
        if (ModCategory.objects.all().count() > 0):
            raise CommandError('La tabla ModCategory contiene instancias')
        if (ModImage.objects.all().count() > 0):
            raise CommandError('La tabla ModImage contiene instancias')

        print('Insertando datos...')

        categories = [
            "Audio",
            "Armour",
            "Buildings",
            "Bug Fixes",
            "Clothing",
            "Crafting",
            "Combat",
            "Cities, Towns, Villages",
            "Creatures",
            "Enviromental",
            "Gameplay",
            "Immersion",
            "Items",
            "Miscellaneous",
            "NPC",
            "Skills and Leveling",
            "Weapons",
            "Models and Textures",
            "Collectables",
            "Animation"
        ]

        for categ in categories:
            ModCategory.objects.create(name=categ)

        print('Listo')
