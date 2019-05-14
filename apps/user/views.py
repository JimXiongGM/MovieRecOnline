from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
# Create your views here.
from django.views import View
from django.contrib.auth.hashers import make_password
from user.forms import LoginForm
from user.models import UserProfile


# 自定义用户验证
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # noinspection PyBroadException
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self, request):
        return render(request, 'index.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            # 如果表单验证通过
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request=request, user=user)
                    return HttpResponseRedirect('/')
                else:
                    return render(request, 'test.html', {'msg': '用户没有激活'})
            else:
                return render(request, 'sign.html', {"msg": "用户名或密码错误"})
        else:
            return render(request, 'index.html', {"msg": login_form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')

class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request,"index.html",{'register_form':register_form})

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("username","")
            try:
                user = UserProfile.objects.get(username = user_name)
            except:
                user = None
            if user != None:
                return render(request, 'duplicat.html', {"msg": "用户名已存在，注册失败"})
            pass_word = request.POST.get("password","")
            Email = request.POST.get("email","")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.password = make_password(pass_word)
            user_profile.email = Email
            user_profile.save()
            return render(request, 'ok.html', {"msg": "注册成功，请登录"})
        else:
            return render(request, 'err.html', {"msg": "注册失败"})

class RegisterForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)
    email = forms.EmailField(required=True)


