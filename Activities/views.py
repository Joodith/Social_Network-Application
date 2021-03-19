from django.shortcuts import render,redirect,get_object_or_404
from Activities import forms
from Activities.models import Post,Comment,Like
from People import views as people_views
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.urls import reverse
from django.views.generic import ListView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import CreateView
from People.models import Profile
from People.views import Suggestions

# Create your views here.

def Postcreate_view(request):
    user=request.user
    if request.method=="POST":
        form=forms.PostForm(request.POST,request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.posted_user=user
            post.save()
            return HttpResponseRedirect(reverse("People:homepage"))
        else:
            messages.add_message(request,messages.ERROR,"Invalid form data")
            return render(request, "Activities/post_create.html", {'form': form})

    else:
        form=forms.PostForm()
        return render(request,"Activities/post_create.html",{'form':form})

class PostListView(ListView):
    model=Post
    template_name="Activities/posts_list.html"
    paginate_by = 10
    ordering =['-post_date']
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        all_posts=Post.objects.all()
        all_comments=[]
        all_likes=[]
        for p in all_posts:
            li=Comment.objects.filter(post=p)
            all_comments.append(li)
            k=Like.objects.filter(post=p)
            all_likes.append(k)
        context['all_posts']=all_posts
        context['all_comments']=all_comments
        context['all_likes']=all_likes
        return context

class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = ''
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(UserPostListView, self).get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        liked = [i for i in Post.objects.filter(posted_user=user) if Like.objects.filter(post=i)]
        commented=[i for i in Post.objects.filter(posted_user=user) if Comment.objects.filter(post=i)]
        context['liked_post'] = liked
        context['comment_post']=commented
        return context

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(posted_user=user).order_by('-date_posted')

def PostDetailView(request,pk):
    post=Post.objects.get(pk=pk)
    if request.user==post.posted_user:
        liked=Like.objects.filter(post=post)
        commented=Comment.objects.filter(post=post)
        return render(request,"Activities/post_detail.html",{'post':post,'liked':liked,'commented':commented})


class PostUpdateView(LoginRequiredMixin,UpdateView):
    model=Post
    fields = ("description", "pic", "tags")
    template_name="Activities/post_create.html"

def post_delete(request,pk):
    post=Post.objects.get(pk=pk)
    if request.user==post.posted_user:
        post.delete()
    return HttpResponseRedirect(reverse('People:profile_page',slug=request.user.profile.slug))


def LikeView(request):
    if request.method=='GET':
        pk = request.GET['pk']
        p=Post.objects.get(pk=pk)
        unlike=False
        try:
            like_obj=Like.objects.get(post=p,liked_user=request.user)
            unlike=True
        except:
            Like.objects.create(post=p,liked_user=request.user)
        if unlike:
            like_obj.delete()
    return people_views.Suggestions(request)

def CommentView(request):
    if request.method=='GET':
        pk=request.GET['pk']
        desc = request.GET['desc']
        post=Post.objects.get(pk=pk)
        print(desc)
        v={'desc':desc}
        user=request.user
        Comment.objects.create(post=post,comment=""+desc,commented_user=user)
        return JsonResponse(v)
    else:
        return HttpResponse("Not get request!")







