# _*_ coding: utf-8 _*_
"""untitled URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
import xadmin
from django.views.static import serve
from untitled.settings import MEDIA_ROOT
from book.views import ThereModelsView, Shows, RegisterView,ActiveUserView,LoginView,Download

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^index/', ThereModelsView.as_view(),name="index"),
    url(r'^show/(?P<book_id>\d+)/$', Shows.as_view(),name="show"),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^media/(?P<path>.*)/$', serve, {"document_root":MEDIA_ROOT}),

    url(r'^register/$',RegisterView.as_view(),name="register"),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),#用户注册
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^download/(?P<book_id>\d+)/$', Download.as_view(), name="download"),
    # url(r'^video/(?P<video_id>\d+)/$', VideoPlayView.as_view(), name="video_play"),  # 课程详情
]
