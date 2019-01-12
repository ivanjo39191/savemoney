from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register',views.register, name='register'),
    path('goodtrack/',views.goodtrack,name='goodtrack'), #我的最愛頁面
    path('adgoodtrack/<int:good_pk>/',views.adgoodtrack,name='adgoodtrack'),  #加入我的追蹤
    path('delgoodtrack/<int:good_pk>/',views.delgoodtrack,name='delgoodtrack'),  #刪除我的追蹤


]
