from django.contrib import admin
from People.models import Profile,FollowRequest,AcceptRequest

# Register your models here.
admin.site.register(Profile)
admin.site.register(FollowRequest)
admin.site.register(AcceptRequest)
