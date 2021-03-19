from django.apps import AppConfig




class PeopleConfig(AppConfig):
    name = 'people'

    def ready(self):
        from django.db.models.signals import post_save
        from django.contrib.auth.models import User
        post_save.connect(sender=User)
