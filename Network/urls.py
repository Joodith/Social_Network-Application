"""Network URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url,include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from django.conf import settings
from People import views
from . import views as super_view
import requests

obj=HttpRequest()
#obj.META['REMOTE_USER']=user
#obj.META['REQUEST_METHOD']="GET"


urlpatterns = [
    url(r'^admin/', admin.site.urls,name='admin'),
    #url('^', include('django.contrib.auth.urls')),
    url(r'^socket/',include('learn_chat.urls',namespace='learn_chat')),
    url(r'^test_cookie/$',super_view.cookie_test,name="cookie_test"),
    url(r'^delete_cookie/$',super_view.cookie_delete,name="delete_cookie"),
    url(r'^$',super_view.StartPage,name="start"),
    url(r'^home/',include('People.urls',namespace="People")),
    url(r'^post/',include('Activities.urls',namespace="Activities")),
    url(r'^register/$',views.UserRegisterView,name="register_user"),
    url(r'^login_user/$',views.UserLoginView,name="login_user"),
    url(r'^birthday/(?P<slug>[-\w]+)/$',views.BirthdayView,name="get_bday"),
    url(r'^verify/(?P<slug>[-\w]+)/$',views.RegisterVerificationView,name="verify_user"),
    #url(r'^login/$',auth_views.LoginView.as_view(template_name=""),name="login"),
    #url(r'^logout/$',auth_views.LogoutView.as_view(template_name=""),name="logout"),
    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(template_name='password_reset.html',email_template_name='password_reset_email.html'), name='password_reset'),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    url(r'^reset/done/$',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
