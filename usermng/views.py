from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .models import *
# Create your views here.


def welcome(request):
    return render(request, 'welcome.html')

def index(request):
    if request.method == 'POST':
        user=authenticate(username=request.POST.get("username"),password=request.POST.get("password"))
        if user:
            login(request,user)
            request.session['username']=request.POST.get("username")#添加session
            return render(request, 'welcome.html', {'username':request.POST.get("username"),'password':request.POST.get('password'),'user':user})
        else:
            return render(request, 'index.html', {'error_message':"用户名或者密码错误"})
    else:
        return render(request, 'index.html')




def register(request):
    if request.method=="POST" and request.POST.getlist("register"):
        username=request.POST.get("username")
        password1=request.POST.get("password")
        password2=request.POST.get("password2")
        if User.objects.filter(username=username):
            error_message="用户名已经存在"
            return render(request,"register.html",{"error_message":error_message})
        elif password1!=password2:
            error_message="两次密码输入不一致，请重新输入"
            return render(request,"register.html",{"error_message":error_message})
        else:#可以注册的情况
            User.objects.create(username=username,password=make_password(password1))
            request.session['username']=username#添加session
            return render(request,"register.html",{"success":True})
    elif request.method == 'POST' and request.POST.getlist('change'):#后端通过getlist()执行不同代码
        password=request.POST.get("password")#原密码
        password2=request.POST.get("password2")#新密码
        password3=request.POST.get("password3")#新密码确认
        if password2==password3:#两次新密码匹配
            user=User.objects.get(username=request.session.get("username"))
            if user.check_password(password):
                User.objects.filter(username=request.session.get("username")).update(password=make_password(password2))
                return render(request,"register.html",{"state":True})
            else:
                error_message="原密码错误，请重新输入"
                return render(request,"register.html",{"state":False,"error_message":error_message})
        else:
            error_message="两次密码不一致，请重新输入"
            return render(request,"register.html",{"state":False,"error_message":error_message})
    else:
        return render(request,"register.html")
def delete(request):
    User.objects.filter(username=request.session.get("username")).delete()  # 注销账号
    return render(request, "index.html", {"error_message": "账号注销成功！"})