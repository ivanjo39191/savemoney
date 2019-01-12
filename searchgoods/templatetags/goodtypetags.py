from django import template
from ..models import GoodsType, GoodsDetail
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
register = template.Library()

@register.simple_tag
def get_good_types(request):
    good_types_count = GoodsType.objects.annotate(good_count=Count('goodsdetail'))
    return good_types_count