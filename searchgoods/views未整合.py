from django.shortcuts import render, get_object_or_404
from .models import GoodsType, GoodsDetail

# Create your views here.
def good_list(request):
    goods = GoodsDetail.objects.all()[:20]
    goodtypes = GoodsType.objects.all()

    context={}
    context['goods'] = goods
    context['goodtypes'] = goodtypes
    return render(request, "goods/good_list.html", context)


def good_type(request,good_type_pk):
    good_type = get_object_or_404(GoodsType, pk=good_type_pk) #獲取分類編號
    good_type_list = GoodsDetail.objects.filter(goodtype=good_type)

    context={}
    context['goods'] = good_type_list
    return render(request,'goods/good_type.html',context)

def good_3cappliance(request):
    
    good_homeappliance_type = get_object_or_404(GoodsType, type_name='家電')
    good_3C_type = get_object_or_404(GoodsType, type_name='3C')
    good_3cappliance_list = GoodsDetail.objects.filter(goodtype__in=[good_homeappliance_type,good_3C_type])

    context={}
    context['goods'] = good_3cappliance_list
    return render(request,'goods/good_type.html',context)
def good_householdsupplies(request):
    
    good_daily_necessities_type = get_object_or_404(GoodsType, type_name='日用品')
    good_houseware_type = get_object_or_404(GoodsType, type_name='居家生活')
    good_makeups_type = get_object_or_404(GoodsType, type_name='美妝')
    good_householdsupplies_list = GoodsDetail.objects.filter(goodtype__in=[good_daily_necessities_type,good_houseware_type,good_makeups_type])

    context={}
    context['goods'] = good_householdsupplies_list
    return render(request,'goods/good_type.html',context)


