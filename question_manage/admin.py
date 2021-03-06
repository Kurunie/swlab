from django.contrib import admin
from .models import *
# Register your models here.
# 修改名称
admin.site.site_header='在线考试系统后台'
admin.site.site_title='在线考试系统'

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id','category','title','optionA','optionB','optionC','optionD','answer','score')

@admin.register(UserEx)
class ExUserAdmin(admin.ModelAdmin):
    list_display = ('id','name','dept','major','type')# 要显示哪些信息
    list_display_links = ('id','name')#点击哪些信息可以进入编辑页面
    search_fields = ['name','dept','major']   #指定要搜索的字段，将会出现一个搜索框让管理员搜索关键词
    list_filter =['name','dept','major']#指定列表过滤器，右边将会出现一个快捷的过滤选项

@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    list_display = ('id', 'tid', 'title', 'major', 'examtime')

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('sid', 'pid', 'grade')

@admin.register(Discussion)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('qid', 'uid', 'title', 'detail')

@admin.register(Reply)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('did', 'uid', 'content')

@admin.register(Fillin)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'title')