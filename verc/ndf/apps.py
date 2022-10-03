from django.apps import AppConfig


class NdfConfig(AppConfig):
    name = 'ndf'
    def ready(self):
        from ndf import receivers
