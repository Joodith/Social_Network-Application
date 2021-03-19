from django.db import models
from django.contrib.auth import settings
from autoslug import AutoSlugField
from django.urls import reverse
import re

User=settings.AUTH_USER_MODEL

# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    profile_pic=models.ImageField(default="blank.JPG",upload_to="profile_pictures/")
    full_name=models.CharField(max_length=50)
    phone_no=models.BigIntegerField(default="123",blank=True)
    email=models.EmailField(null=True,blank=True)
    bday=models.DateField(null=True)
    slug=AutoSlugField(populate_from='user')
    bio=models.TextField(max_length=200,blank=True)
    requested_to=models.ManyToManyField('Profile',related_name="req_people",through="FollowRequest",null=True,blank=True,symmetrical=False,default=None)
    accepted_from=models.ManyToManyField('Profile',related_name="acc_people",through="AcceptRequest",null=True,blank=True,symmetrical=False,default=None)


    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('People:profile_page',kwargs={'slug':self.slug})



class FollowRequest(models.Model):
    to_user=models.ForeignKey('Profile',related_name="to_user",on_delete=models.CASCADE)
    from_user=models.ForeignKey('Profile',related_name="from_user",on_delete=models.CASCADE)


    def __str__(self):
        return "from {} to {}".format(self.from_user.user.username,self.to_user.user.username)

class AcceptRequest(models.Model):
    accept_to = models.ForeignKey('Profile', related_name="accept_to", on_delete=models.CASCADE)
    accept_by = models.ForeignKey('Profile', related_name="accept_by", on_delete=models.CASCADE)

    def __str__(self):
        return "accepted {} from {}".format(self.accept_to.user.username, self.accept_by.user.username)




