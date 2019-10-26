from django.apps import AppConfig


class LikesConfig(AppConfig):
    name = 'likes'
    def ready(self):
    	from . import signals