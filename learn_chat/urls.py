from django.conf.urls import url
from learn_chat import views
app_name='learn_chat'

urlpatterns=[
    url(r'^chat_index/$',views.index,name="index"),
]