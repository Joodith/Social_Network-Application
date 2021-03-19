from django.shortcuts import render
from People import views
from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.views.generic import TemplateView


def  StartPage(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login_user'))
    else:
        return HttpResponseRedirect(reverse('login_user'))

def cookie_test(request):
    request.session.set_test_cookie()
    return HttpResponse("Test cookie set!!")

def cookie_delete(request):
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
        response="Test cookie deleted!"
    else:
        response="Browser is not supporting cookies!"
    return HttpResponse(response)
