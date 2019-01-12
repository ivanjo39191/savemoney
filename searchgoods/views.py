from django.shortcuts import render, get_object_or_404
from .models import GoodsType, GoodsDetail
from django.core.paginator import Paginator

def good_common_data(request, good_all_list):
    #將資料進行分頁
    paginator = Paginator(good_all_list,9)
    #獲取url頁面參數
    page_num = request.GET.get('page',1)
    #自動識別頁碼
    page_of_goods = paginator.get_page(page_num)
    #當前頁碼
    current_page_num = page_of_goods.number
    #當前頁碼的資料
    currnt_good_list = page_of_goods.object_list
    #頁碼範圍
    page_range = list(range(max(1,current_page_num-2),current_page_num)) +\
                 list(range(current_page_num,min(paginator.num_pages,current_page_num+2)+1))
    #加入省略符號
    if page_range[0] -1 >= 2:
        page_range.insert(0, '...')
    if page_range[-1] + 2 <= paginator.num_pages:
        page_range.append('...')
    #加入首頁末頁
    if page_range[0] != 1:
        page_range.insert(0,1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)


    
    goodtypes = GoodsType.objects.all()
    context={}
    context['goods'] = currnt_good_list
    context['goodtypes'] = goodtypes
    context['page_range'] = page_range
    context['page_of_goods'] = page_of_goods
    return context

def price_order(request, good_all_list, order):

    if order == 'cheap':
        good_all_list = good_all_list.order_by('goodprice')
    if order == 'expensive':
        good_all_list = good_all_list.order_by('-goodprice')
    if order == 'momo':
        good_all_list = good_all_list.filter(goodshop='momo購物網')
    if order == 'PChome':
        good_all_list = good_all_list.filter(goodshop='PChome購物中心')
    return good_all_list


# Create your views here.
def good_list(request,order=None):


    good_all_list = GoodsDetail.objects.all()
    good_all_list = price_order(request, good_all_list, order)
    context = good_common_data(request, good_all_list)

    return render(request, "goods/good_list.html", context)


def good_type(request,good_type_pk,typeorder=None):
    good_type = get_object_or_404(GoodsType, pk=good_type_pk) #獲取分類編號
    good_type_list = GoodsDetail.objects.filter(goodtype=good_type)
    good_type_list = price_order(request, good_type_list, typeorder)
    context={}
    context = good_common_data(request, good_type_list)
    context['type'] = good_type
    return render(request,'goods/good_type.html',context)

def good_3cappliance(request,order=None):
    
    good_homeappliance_type = get_object_or_404(GoodsType, type_name='家電')
    good_3C_type = get_object_or_404(GoodsType, type_name='3C')
    good_3cappliance_list = GoodsDetail.objects.filter(goodtype__in=[good_homeappliance_type,good_3C_type])
    good_3cappliance_list = price_order(request, good_3cappliance_list, order)

    context={}

    context = good_common_data(request, good_3cappliance_list)
    return render(request,'goods/good_3cappliance.html',context)
def good_householdsupplies(request,order=None):
    
    good_daily_necessities_type = get_object_or_404(GoodsType, type_name='日用品')
    good_houseware_type = get_object_or_404(GoodsType, type_name='居家生活')
    good_makeups_type = get_object_or_404(GoodsType, type_name='美妝')
    good_householdsupplies_list = GoodsDetail.objects.filter(goodtype__in=[good_daily_necessities_type,good_houseware_type,good_makeups_type])
    good_householdsupplies_list = price_order(request, good_householdsupplies_list, order)
    context={}
    context = good_common_data(request, good_householdsupplies_list)
    return render(request,'goods/good_householdsupplies.html',context)



