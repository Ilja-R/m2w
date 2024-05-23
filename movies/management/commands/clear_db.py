from django.core.management.base import BaseCommand
from django.db import transaction
from django.apps import apps


class Command(BaseCommand):
    help = 'Clears all data from the database'

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            for model in apps.get_models():
                model.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleared the database'))
