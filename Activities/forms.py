from django import forms
from Activities.models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=("description","pic","tags")
    """def save(self,usr,commit=True):
        post=super(PostForm,self).save(commit=False)
        post.posted_user=usr
        if commit:
            post.save()
        return post"""


