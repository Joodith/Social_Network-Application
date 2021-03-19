from django.conf.urls import url
from Activities import views
app_name="Activities"

urlpatterns=[
    url(r'^feed/$',views.PostListView.as_view(),name="list_posts"),
    url(r'^create_post/$',views.Postcreate_view,name="post_create"),
    url(r'^post_details/(?P<pk>\d+)/$',views.PostDetailView,name="detail_post"),
    url(r'^post_update/(?P<pk>\d+)/$',views.PostUpdateView.as_view(),name="update_post"),
    url(r'^post_delete/(?P<pk>\d+)/$',views.post_delete,name="del_post"),
    url(r'^like_post/$',views.LikeView,name="like_post"),
    url(r'^comment_on_post/$',views.CommentView,name="comment_post"),
]