from django.apps import AppConfig
from betcnow.signals import handlers
from django.db.models.signals import post_migrate


class BetcnowConfig(AppConfig):
    name = 'betcnow'

    def ready(self):
        post_migrate.connect(handlers.create_notice_types, sender=self)
