from django.shortcuts import render,redirect
from .forms import LoginForm,RegisterForm
from django.urls import reverse
from django.contrib import auth
from .models import Profile
from django.contrib.auth.models import User
from searchgoods.models import  GoodsType, GoodsDetail
from django.core.paginator import Paginator

def login(request):
    if request.method =='POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from',reverse('home')))
    else:
        login_form = LoginForm()
    context = {}
    context['login_form'] = login_form
    return render(request, "user/login.html",context)

def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from',reverse('home')))


def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username =  register_form.cleaned_data['username']
            email =register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            user = User()
            user.username =username
            user.email = email
            user.set_password(password)
            user.save()
            user = auth.authenticate(username=username,password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from',reverse('home')))
    else:
        register_form = RegisterForm()
    context = {}
    context['register_form'] = register_form
    return render(request, "user/register.html", context)

def goodtrack(request):
    goodtrack = User.objects.get(username=request.user)
    context={}
    context['goodtrack'] = goodtrack
    return render(request, "user/goodtrack.html", context)

def adgoodtrack(request, good_pk=None):
    userinfo = User.objects.get(username=request.user)
    profile, created = Profile.objects.get_or_create(user=request.user)
    goodtrack_list = userinfo.goodtrack()
    good = GoodsDetail.objects.get(id=good_pk)
    good_type = GoodsType.objects.get(type_name=good.goodtype)
    flag = True
    for track in goodtrack_list:
        if good.goodname == track[0]:
            flag = False
            break
    if flag:
        tracklist=[]
        tracklist.append(good.goodname)
        tracklist.append(good.goodprice)
        tracklist.append(good.goodshop)
        tracklist.append(good_type.type_name)
        tracklist.append(good.goodlink)
        tracklist.append(good.goodimglink)
        goodtrack_list.append(tracklist)
        profile.goodtrack = goodtrack_list
        profile.save()

    return redirect(request.GET.get('from',reverse('home')))

def delgoodtrack(request, good_pk=None):
    userinfo = User.objects.get(username=request.user)
    profile, created = Profile.objects.get_or_create(user=request.user)
    goodtrack_list = userinfo.goodtrack()
    del goodtrack_list[int(good_pk)] #從我的最愛中移除該文章，用計數器的方式取得list的項數
    profile.goodtrack = goodtrack_list
    profile.save()

    return redirect(request.GET.get('from',reverse('home')))

