from django.contrib import admin
from django.urls import include,path
from . import crawler,views
from haystack.urls import SearchView
from haystack.query import SearchQuerySet
from .models import GoodsDetail,GoodsType

pricelow = SearchQuerySet().models(GoodsDetail).order_by('goodprice')

urlpatterns = [
    path('momocrawler', crawler.momocrawler, name='momocrawler'),
    path('pchomecrawler', crawler.pchomecrawler, name='pchomecrawler'),
    path('good_list/<order>',views.good_list,name='good_list'),
    path('type/<int:good_type_pk>/<typeorder>/',views.good_type,name='good_type'),
    path('good_3cappliance/<order>',views.good_3cappliance,name='good_3cappliance'),
    path('good_householdsupplies/<order>',views.good_householdsupplies,name='good_householdsupplies'),
    path('search/',SearchView(searchqueryset=pricelow), name='haystack_search'),

]
