from django.shortcuts import render,get_object_or_404,redirect
from People.models import Profile,FollowRequest,AcceptRequest
from Activities.models import Post,Like
from django.contrib.auth.models import User
from People import forms
from People.authy_api import send_verification_code,verify_code_sent
from People.validations import validating_number
from django.core.validators import ValidationError,validate_email
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
from django.urls import reverse,reverse_lazy
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.generic import UpdateView,ListView,RedirectView,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail,EmailMultiAlternatives
from django.contrib.auth import settings
from django.template.loader import get_template
import json
import random

# Create your views here.
#   Registering Users
#   Verification Code in phone/mail
#   Profile show/Profile update
#   Reset Password
#   Suggestions
#   send request
#   accept_request
#   cancel request
#   delete request
#   Viewing other's profile
#   Follower/Following list display
#   Search for usernames
#   unfollow person
def UserLoginView(request):
    if request.method=="POST":
        form=forms.UserLoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=User.objects.get(username=username)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            user_auth=authenticate(username=username,password=password)

            #print(user)
            #print(user.check_password(password))
            if user.check_password(password):
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect(reverse('People:homepage'))
            else:
                messages.add_message(request, messages.ERROR, "Invalid username or password")
                return render(request, "login.html", {'form': form})

        else:
            messages.add_message(request,messages.ERROR,"Invalid form details!")
            return render(request,"login.html",{'form':form})
    else:
        form=forms.UserLoginForm()
        return render(request, "login.html", {'form': form})



def UserRegisterView(request):
    if request.method=="POST":
        basic_form=forms.UserRegisterForm(data=request.POST)
        other_details_form=forms.UserExtraDetailsForm(data=request.POST)
        cont =request.POST.get('contact')
        mail = False
        number = False
        if '@' not in cont:
            number = True
        else:
            mail = True
        if mail:
            validate_email(cont)
        if number:
            validating_number(cont)
        if not mail and not number:
            raise ValidationError(_("Enter valid phone number or email!"), code="invalid")
        if basic_form.is_valid() and other_details_form.is_valid():
            user=basic_form.save()
            profile = Profile.objects.create(user=user)
            #other_details_form.save()
            if '@' in str(cont):
                email=cont
                profile.email=email
            else:
                num=0
                for i in str(cont):
                    num=num*10+int(i)

                phone_no=num
                profile.phone_no=phone_no
            profile.full_name=other_details_form.cleaned_data['full_name']
            profile.save()
            return HttpResponseRedirect(reverse('get_bday',kwargs={'slug':profile.slug}))
        else:
            messages.error(request,'Invalid data entered!')
    else:
        basic_form = forms.UserRegisterForm()
        other_details_form = forms.UserExtraDetailsForm()
    return render(request,'register.html',{'basic_form':basic_form,'other_form':other_details_form})

def BirthdayView(request,**kwargs):
    if request.method=="POST":
        form=forms.BirthdayForm(request.POST)
        if form.is_valid():
            profile=Profile.objects.get(slug=kwargs.get('slug'))
            profile.bday=form.cleaned_data['bday']
            profile.save()
            try:
                response = send_verification_code(profile)
            except:
                messages.add_message(request, messages.ERROR, 'Click Resend otp to get the otp again!!')
                return HttpResponse("OTP PAGE NOT FOUND")
            data = json.loads(response.text)
            print(data)
            pr=Profile.objects.get(slug=kwargs.get('slug'))
            if data['success'] == True:
                request.method = "GET"
                kwargs = {
                    'prof':pr,
                }
                return RegisterVerificationView(request, **kwargs)

            else:
                messages.add_message(request, messages.ERROR, data['message'])
                return HttpResponse("ERROR FOUND")
        else:
            messages.error(request,"Invalid birthday date!")
    else:
        form=forms.BirthdayForm()
    return render(request,"bday.html",{'form':form})




def RegisterVerificationView(request,**kwargs):
    if request.method=="POST":
        profile = Profile.objects.get(slug=kwargs.get('slug'))
        user=profile.user
        form = forms.VerifyCodeForm(request.POST)
        if form.is_valid():
            resp=verify_code_sent(form.cleaned_data['otp'],profile)
            dat=json.loads(resp.text)
            if dat['success']==True:
                login(request,user)
                return HttpResponseRedirect(reverse('People:homepage'))
            else:
                messages.add_message(request,messages.ERROR,dat['message'])
                return HttpResponse(messages)
        else:
            messages.add_message(request, messages.ERROR,'Invalid form details')
            return HttpResponse(messages)
    else:
        form = forms.VerifyCodeForm()
        profile=kwargs['prof']
        return render(request,"register_confirm.html",{'form':form,'profile':profile})


class EditProfileView(UpdateView):
    model=Profile
    fields = ('full_name','user','bday','profile_pic','bio','email','phone_no')
    template_name="People/profile_edit.html"

def Suggestions(request):
    all_users=Profile.objects.exclude(user=request.user)
    my_friends=[]
    cur_user=request.user.profile
    requested_me =cur_user.requested_to.all()
    r=FollowRequest.objects.filter(from_user=request.user.profile)
    my_requests=[]
    button_status="Follow"
    for i in r:
        my_requests.append(i.to_user)
        if len(FollowRequest.objects.filter(from_user=request.user.profile).filter(to_user=i.to_user))==1:
            button_status="Requested"

    m=AcceptRequest.objects.filter(accept_by=request.user.profile)
    acc=[]
    for i in m:
        acc.append(i.accept_to)
        if len(AcceptRequest.objects.filter(accept_to=request.user.profile).filter(accept_by=i.accept_by))==1:
            button_status="Following"
    accepts=cur_user.accepted_from.all()
    #print(my_requests)
    #print(accepts)
    show_people=[]
    sent_requests=[]

    count=0
    for p in all_users:
        if p not in requested_me and p not in accepts and p not in acc:
            if p!=cur_user:
                li=[p]
                show_people.append(li)
                button_status="Follow"

                if len(AcceptRequest.objects.filter(accept_to=request.user.profile).filter(accept_by=p)) == 1:
                    button_status = "Following"
                if len(FollowRequest.objects.filter(from_user=request.user.profile).filter(to_user=p)) == 1:
                    button_status = "Requested"
                show_people[count]+=[button_status]
                count+=1
    post_list=Post.objects.all().order_by('post_date')
    #post_list=Paginator(li,10)



    """random_list=random.sample(list(all_users),min(len(list(all_users)),10))
    for ran in random_list:
        if ran in show_people:
            random_list.remove(ran)
    show_people+=random_list"""
    """for k in accepts:
        frnds=k.accepted_from.all()
        for n in frnds:
            if n not in show_people and n!=cur_user:
                show_people.append(n)"""
    pkvalues=[]
    for i in post_list:
        pkvalues.append(i.pk)
    json_pkvalues=json.dumps(pkvalues)
    like_list=[]
    for i in request.user.likes.all():
        like_list.append(i.post)
    return render(request,"People/suggestions.html",{'suggestions':show_people,'cur_user':request.user,'post_list':post_list,'json_pkvalues':json_pkvalues,'like_list':like_list})


class SendRequestView(LoginRequiredMixin,RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('People:homepage')

    def get(self, request, *args, **kwargs):
        self.button_status = "Follow"
        requested_user = get_object_or_404(Profile, pk=self.kwargs.get('pk'))
        try:
            FollowRequest.objects.create(from_user=request.user.profile,to_user=requested_user)
            self.button_status="Requested"

        except:
            messages.add_message(request,messages.ERROR,"User not found!")
            return HttpResponse("User not found!")
        recipient = requested_user.user.email
        subject = "Friend Request sent"
        with open(settings.BASE_DIR + "/People/templates/People/view_request.txt") as fl:
            tell_message = fl.read()
        message = EmailMultiAlternatives(subject=subject,
                                         body=tell_message, from_email=settings.EMAIL_HOST_USER, to=[recipient])
        html_template = get_template("People/view_request.html").render(context={'cur_user':self.request.user})
        message.attach_alternative(html_template, "text/html")
        message.send()




        return super().get(request,*args,**kwargs)



def MyRequestList(request,remove_req=None,**kwargs):
    template_name="People/request_list.html"
    try:
        user=Profile.objects.get(slug=kwargs.get('slug'))
        req_list=FollowRequest.objects.filter(to_user=user)
    except:
        pass
    cur_user=Profile.objects.get(slug=kwargs.get('slug'))
    if remove_req!=None:
        req_list=req_list.exclude(from_user=remove_req.from_user,to_user=remove_req.to_user)
    return render(request,template_name,{'request_list':req_list,'cur_user':request.user})



@login_required
def accept_request(request,pk):
    from_user=get_object_or_404(Profile,pk=pk)
    already=False
    try:
        d=AcceptRequest.objects.get(accept_to=request.user.profile,accept_by=from_user)
        already=True
    except:
        frequest=AcceptRequest.objects.create(accept_to=from_user,accept_by=request.user.profile)
        frequest.save()
    myself=request.user.profile
    to_del=FollowRequest.objects.get(from_user=from_user,to_user=myself)
    follow_back=to_del.from_user
    to_del.delete()
    recipient =request.user.email
    subject = "Friend Request sent"
    with open(settings.BASE_DIR + "/People/templates/People/view_request.txt") as fl:
        tell_message = fl.read()
    message = EmailMultiAlternatives(subject=subject,
                                     body=tell_message, from_email=settings.EMAIL_HOST_USER, to=[recipient])
    html_template = get_template("People/request_accept_email.html").render(context={'cur_user': request.user})
    message.attach_alternative(html_template, "text/html")
    message.send()

    return render(request,"People/other_profile.html",{'follow_back':follow_back,'cur_user':request.user,'already':already})

@login_required
def delete_accept(request,pk):
    from_person=get_object_or_404(Profile,pk=pk)
    frequest=FollowRequest.objects.get(from_user=from_person,to_user=request.user.profile)
    kwargs={
        'slug':request.user.profile.slug
    }
    return MyRequestList(request,remove_req=frequest,**kwargs)

@login_required
def cancel_request(request,pk):
    to_person = get_object_or_404(Profile, pk=pk)
    frequest = FollowRequest.objects.filter(from_user=request.user.profile, to_user=to_person)
    frequest.delete()
    return HttpResponseRedirect(reverse('People:homepage'))

@login_required
def delete_friend(request,id):
    from_user=get_object_or_404(User,pk=id)
    frequest=FollowRequest.objects.filter(from_user=from_user, to_user=request.user)
    request.user.profile.friends.remove(from_user)
    frequest.delete()
    return HttpResponseRedirect()

@login_required
def ProfileView(request,slug):
    prof=Profile.objects.get(user=request.user)
    following=prof.accepted_from.all()
    followers =[]
    req_obj=AcceptRequest.objects.filter(accept_by=request.user.profile)
    for i in req_obj:
        followers.append(i.accept_to)
    print(len(followers))
    context={
        'req':req_obj,
        'followers':followers,
        'following':following,
        'cur_user':request.user,
    }
    return render(request,"People/profile.html",context)

@login_required
def search(request):
    query=request.GET.get('search')
    obj_list=User.objects.filter(username__icontains=query)
    return render(request,"People/search_list.html",{'obj_list':obj_list,'cur_user':request.user})

class FollowerListView(ListView):
    model=Profile
    template_name="People/followers.html"



    def get_queryset(self):
        self.followers = []
        try:
            req_obj = AcceptRequest.objects.filter(accept_by=self.request.user.profile)
            for i in req_obj:
                self.followers.append(i.accept_to)
        except:
            pass

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['followers']=self.followers
        context['cur_user']=self.request.user
        return context


class FollowingListView(ListView):
    model = Profile
    template_name = "People/following.html"

    def get_queryset(self):
        try:
            prof = Profile.objects.get(user=self.request.user)
            self.following = prof.accepted_from.all()
        except:
            self.following= []


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['following'] = self.following
        context['cur_user'] = self.request.user
        return context











































