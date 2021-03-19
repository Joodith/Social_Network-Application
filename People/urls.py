from django.conf.urls import url
from People import views
app_name="People"

urlpatterns=[
    url(r'^$',views.Suggestions,name="homepage"),
    url(r'^profile/(?P<slug>[-\w]+)/$',views.ProfileView,name="profile_page"),
    url(r'^edit_profile/(?P<pk>\d+)/$',views.EditProfileView.as_view(),name="edit_profile"),
    url(r'^show_requests/(?P<slug>[-\w]+)/$',views.MyRequestList,name="list_request"),
    url(r'^send_request/(?P<slug>[-\w]+)/(?P<pk>\d+)/$',views.SendRequestView.as_view(),name="req_send"),
    url(r'^accept_request/(?P<pk>\d+)/$',views.accept_request,name="req_accept"),
    url(r'^delete_request/(?P<pk>\d+)/$',views.delete_accept,name="req_del"),
    url(r'^cancel_request/(?P<pk>\d+)/$',views.cancel_request,name="req_cancel"),
    url(r'^unfollow/(?P<pk>\d+)/$',views.delete_friend,name="unfollow"),
    url(r'^followers/(?P<slug>[-\w]+)/$',views.FollowerListView.as_view(),name="follo_wer"),
    url(r'^following/(?P<slug>[-\w]+)/$',views.FollowingListView.as_view(),name="follo_wing"),
    url(r'^search_users/$',views.search,name="search_users"),

]
