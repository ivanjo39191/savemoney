from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db import models
import ast
 #自定義field

class ListField(models.TextField):

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection, context):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return str(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #一對一關聯
    goodtrack = ListField(blank=True)
    def __str__(self): #定義物件名稱
        return self.user.username

def get_goodtrack(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.goodtrack
    else:
        return ''
#將list賦值給User模型
User.goodtrack = get_goodtrack