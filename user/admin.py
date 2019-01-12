from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
 
#顯示Profile模型
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','goodtrack')
 
#將Profile添加至User模型
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
 
# 定義新的Admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, ) #插入Profile
    list_display = ('username','goodtrack','email','is_staff','is_active','is_superuser')
    def goodtrack(self, obj): #定義nickname欄位顯示的內容
        return obj.profile.goodtrack
    goodtrack.short_description = '追蹤清單' #介面顯示為中文
 
 
# 重新註冊Admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)