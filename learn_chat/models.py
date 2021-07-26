from django.db import models
from django.contrib.auth import settings
from channels import Group

# Create your models here.
class ChatRoom(models.Model):
    title=models.CharField(max_length=200,unique=True)
    chat_users=models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True)

    @property
    def websocket_group(self):
        return Group("room-%s"%self.id)


    def __str__(self):
        return self.title
