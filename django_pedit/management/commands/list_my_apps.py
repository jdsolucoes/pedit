# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = "List the apps for Pedit's parser"

    def handle(self, *args, **options):
        for app in settings.INSTALLED_APPS:
            # Django's app, not important
            if 'django' not in app:
                self.stdout.write(app)
