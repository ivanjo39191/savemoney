from django.shortcuts import render
from searchgoods.models import GoodsType, GoodsDetail



def home(request):


    context={}

    return render(request, "home.html", context)
