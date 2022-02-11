# -*- coding: utf-8 -*-
__author__ = 'mybbzy'

import xadmin
from .models import EmailVerifyRecord, UserProfile, ThereModels,ObjModels

#user设置页面显示
#其中list_dispaly显示列表显示的内容
#list_filter是过滤器的设置
#search_filelds是搜索内容的设置
#在搜索中需要注意外键的搜索设置：code__name表示按照外键的名称进行查找

# 开启主题功能
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


#修改页面显示功能
class GlobalSetting(object):
    site_title = "3D后台管理系统";#修改的是左上角的信息输出
    site_footer = "3D后台管理系统"#修改的是最下方的信息输出
    menu_style = "3D"#收缩显示功能


class EmailVerifyRecordAdmin(object):
    list_display = ['code','email','send_type','send_time']#表示在页面中显示时，出现的内容标题
    search_fields = ['code','email','send_type']#搜索框功能，数组里面的数据表示的是可以进行搜索的类型
    list_filter = ['code','email','send_type','send_time']#过滤器
    model_icon = 'fa fa-envelope'


class ThereModelsAdmin(object):
    list_display = ['model_name','up_time','download_times']
    list_filter = ['model_name','download_times']
    search_fields = ['model_name','up_time','download_times']
    model_icon = 'fa fa-group'


class ObjModelsAdmin(object):
    list_display = ['obj', 'add_time']
    list_filter = ['obj__there_file']
    search_fields = ['obj', 'add_time']


#将管理器与model进行注册关联
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(ThereModels, ThereModelsAdmin)
xadmin.site.register(ObjModels, ObjModelsAdmin)
# xadmin.site.register(views.BaseAdminView, BaseSetting)
# xadmin.site.register(views.CommAdminView,GlobalSetting)
# xadmin.site.register(UserProfile,UserProfileAdmin)