# _*_ coding: utf-8 _*_
import os,re
from django.shortcuts import render
from django.views.generic.base import View#表示对类进行逻辑编写
from django.http import HttpResponse,HttpResponseRedirect, StreamingHttpResponse
from django.contrib.auth.hashers import make_password
from .forms import LoginForm,RegisterForm
from django.contrib.auth import authenticate,login,logout
from django.core.urlresolvers import reverse
from django.http import FileResponse

from .models import ThereModels,ObjModels, UserProfile,UserMessage,EmailVerifyRecord
from utils.email_send import send_register_email

# Create your views here.


class ThereModelsView(View):
    def get(self,request):
        model_name = ThereModels.objects.all()
        return render(request,"index.html",{
            "model_name":model_name,
        })


class Shows(View):

    def get(self,request,book_id):
        objs = ObjModels.objects.get(obj=int(book_id))
        book = objs.obj
        mtl_path = book.there_file
        name_m = str(mtl_path).split('/',4)[-1]
        name = str(name_m).split('.')[0]
        m_path = str(mtl_path).split('/',4)[0:3]
        mm_path = '/'.join(m_path)
        print(mm_path)

        obj_path = objs.three_file
        o_path = str(obj_path).split('/', 4)[0:3]
        oo_path = '/'.join(o_path)

        return render(request, "base.html", {
            "base_name" : name,
            "path" : mm_path,
            "book":book,
            "obj_path":oo_path,
            "book_id" : book_id,
        })


class Download(View):
    def get(self, request,book_id):
        book = ThereModels.objects.get(id=int(book_id))

        def file_iterator(file, chunk_size=512):
            with open(file) as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break

        file = book.there_file
        response = StreamingHttpResponse(file_iterator(file.path))
        response['Content-Type'] = 'application/octet-stream'
        book_name = book.model_name
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(book_name)
        return response



class RegisterView(View):

    def get(self,request):
        # 添加验证码
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    def post(self,request):
        register_form = RegisterForm(request.POST);#实例化form

        if register_form.is_valid():
            user_name = request.POST.get("email","")#获取页面登录时的username
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"msg": "该用户已经存在"})
            pass_word = request.POST.get("password","")#获取页面登录时的password
            user_profile = UserProfile();
            user_profile.username = user_name#设置页面信息中的username给数据库
            user_profile.email =user_name#设置页面信息中的email给数据库
            user_profile.is_active = False#设置为邮箱未激活状态
            user_profile.password = make_password(pass_word)#make_password表示将明文的密码改为不可阅读的密码
            user_profile.save()#存进数据库

            #写入欢迎注册消息
            user_message = UserMessage();
            user_message.user = user_profile.id
            user_message.message = "欢迎注册慕学在线网"
            user_message.save()

            #发送邮件
            send_register_email(user_name,"register")
            return render(request, "login.html")
        else:
            return render(request, "register.html",{"register_form":register_form})


#邮箱激活
class ActiveUserView(View):
    #active_code表示默认给发送者发送的字符串，目的是为了安全性能的提高
    def get(self,request,active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)

        if all_records:
            for record in all_records:
                email = record.email;
                user = UserProfile.objects.get(email=email);
                #此方法最终要的就是设置该值为True
                user.is_active = True;
                user.save()
        else:
            return render(request,"active_fail.html")
        return render(request,"login.html")


class LoginView(View):
    def get(self,request):
        return render(request, "login.html", {})
    def post(self,request):
        login_form = LoginForm(request.POST);
        # 这里的else表示的是必要信息的填写
        if login_form.is_valid():
            # 获取登录时的username和password字段内容
            user_name = request.POST.get("username", "");
            pass_word = request.POST.get("password", "");
            # html中的csrf_token成功返回user对象,失败返回null
            user = authenticate(username=user_name, password=pass_word);
            if user is not None:
                #这里是对邮件是否被激活
                if user.is_active:
                    #进行登录验证
                    #login中还存在session的存储，就是给本次请求一个特定的id，存放在数据库表内。
                    login(request, user);
                    # 登陆成功跳转页面
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request,"login.html",{"msg":"用户未激活"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误！"})
        else:
            # 否则跳转到本页面并返回错误信息
            return render(request, "login.html", {"login_form":login_form})


# # 文件下载
# class Download(View):
#     mtl_path = ''
#     def get(self,request,bo_id):
#         objs = ObjModels.objects.get(obj=int(bo_id))
#         book = objs.obj
#         mtl_path = book.there_file
#
#
# def download_file(request,mtl_path):
#     def file_iterator(file, chunk_size=512):
#         with open(file) as f:
#             while True:
#                 c = f.read(chunk_size)
#                 if c:
#                     yield c
#                 else:
#                     break
#
#     file = "http://127.0.0.1:8000/media/"+mtl_path
#     response = StreamingHttpResponse(file_iterator(file))
#     response['Content-Type'] = 'application/octet-stream'
#     response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file)
#     return response