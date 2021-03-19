from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
# Create your models here.
class Post(models.Model):
    description=models.CharField(max_length=500,null=True,blank=True)
    post_date=models.DateTimeField(default=timezone.now())
    pic=models.ImageField(upload_to="posts/")
    posted_user=models.ForeignKey(settings.AUTH_USER_MODEL,related_name="posts",on_delete=models.CASCADE)
    tags=models.CharField(max_length=200,blank=True)

    def __str__(self):
        return "{} posted {}".format(self.posted_user.username,self.description)

    def get_absolute_url(self):
        return reverse('Activities:detail_post',kwargs={'pk':self.pk})

class Comment(models.Model):
    post=models.ForeignKey("Post",related_name="commented",on_delete=models.CASCADE)
    commented_user=models.ForeignKey(settings.AUTH_USER_MODEL,related_name="commented",on_delete=models.CASCADE)
    comment=models.CharField(max_length=500,blank=True)
    comment_date=models.DateTimeField(default=timezone.now())

    def __str__(self):
        return "{} commented {}".format(self.commented_user.username,self.comment)

class Like(models.Model):
    post=models.ForeignKey("Post",related_name="likes",on_delete=models.CASCADE)
    liked_user=models.ForeignKey(settings.AUTH_USER_MODEL,related_name="likes",on_delete=models.CASCADE)

    def __str__(self):
        return "{} liked".format(self.liked_user.username)

