from django.apps import AppConfig


class CommentConfig(AppConfig):
    name = 'comment'
    def ready(self):
    	from . import signals
