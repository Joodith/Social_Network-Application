from django.shortcuts import render
from learn_chat.models import ChatRoom

# Create your views here.
def index(request):
    rooms=ChatRoom.objects.order_by("title")
    return render(request,"learn_chat/index.html",{'rooms':rooms})
