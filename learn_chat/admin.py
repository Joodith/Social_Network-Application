from django.contrib import admin
from learn_chat.models import ChatRoom

# Register your models here.
admin.site.register(
   ChatRoom,
   list_display=['id','title']
)
