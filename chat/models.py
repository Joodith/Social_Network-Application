from django.db import models
from django.contrib.auth import settings

# Create your models here.
class PublicChatRoom(models.Model):
    title=models.CharField(max_length=200,unique=True)
    users=models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True)

    def __str__(self):
        return self.title
    def connect_user(self,user):
        user_added=False
        if user not in self.users.all():
            self.users.add(user)
            user_added=True
        elif user in self.users.all():
            user_added=True
        return user_added

    def disconnect_user(self,user):
        user_removed=False
        if user in self.users.all():
            self.users.remove(user)
            user_removed=True
        return user_removed

    @property
    def group_name(self):
        return f"PublicChatRoom-{self.id}"

class PublicChatManager(models.Manager):
    def by_room(self,room):
        s=PublicChatMessage.objects.filter(room=room).order_by("-time")
        return s

class PublicChatMessage(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    room=models.ForeignKey(PublicChatRoom,on_delete=models.CASCADE)
    content=models.TextField(blank=False)
    time=models.DateTimeField(auto_now_add=True)

    objects=PublicChatManager()
    def __str__(self):
        return self.content

