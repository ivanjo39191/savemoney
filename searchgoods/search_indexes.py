from searchgoods.models import GoodsDetail,GoodsType
from haystack import indexes
from haystack.query import SearchQuerySet

class GoodsDetailIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    goodprice = indexes.IntegerField(model_attr='goodprice') 


    def get_model(self):
        return GoodsDetail

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()