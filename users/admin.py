from email import message
from mailbox import Message
from django.contrib import admin
from django.apps import AppConfig



from .models import Profile, Skill,Message

# Register your models here.

admin.site.register(Profile)  
admin.site.register(Skill)
admin.site.register(Message)

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        import users.signals  # noqa: F401