from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, StreamingHttpResponse, FileResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .models import *


# Create your views here.


def welcome(request):
    return render(request, 'welcome.html')


def index(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST.get("username"), password=request.POST.get("password"))
        if user:
            login(request, user)
            request.session['username'] = request.POST.get("username")  # 添加session
            return render(request, 'welcome.html',
                          {'username': request.POST.get("username"), 'password': request.POST.get('password'),
                           'user': user})
        else:
            return render(request, 'index.html', {'error_message': "用户名或者密码错误"})
    else:
        return render(request, 'index.html')


def register(request):
    if request.method == "POST" and request.POST.getlist("register"):
        username = request.POST.get("username")
        password1 = request.POST.get("password")
        password2 = request.POST.get("password2")
        if User.objects.filter(username=username):
            error_message = "用户名已经存在"
            return render(request, "register.html", {"error_message": error_message})
        elif password1 != password2:
            error_message = "两次密码输入不一致，请重新输入"
            return render(request, "register.html", {"error_message": error_message})
        else:  # 可以注册的情况
            User.objects.create(username=username, password=make_password(password1))
            request.session['username'] = username  # 添加session
            return render(request, "register.html", {"success": True})
    else:
        return render(request, "register.html")


def chpwd(request):
    if request.method == 'POST' and request.POST.getlist('change'):  # 后端通过getlist()执行不同代码
        password = request.POST.get("password")  # 原密码
        password2 = request.POST.get("password2")  # 新密码
        password3 = request.POST.get("password3")  # 新密码确认
        if password2 == password3:  # 两次新密码匹配
            user = User.objects.get(username=request.session.get("username"))
            if user.check_password(password):
                User.objects.filter(username=request.session.get("username")).update(password=make_password(password2))
                return render(request, "chpwd.html", {"state": True})
            else:
                error_message = "原密码错误，请重新输入"
                return render(request, "chpwd.html", {"state": False, "error_message": error_message})
        else:
            error_message = "两次密码不一致，请重新输入"
            return render(request, "chpwd.html", {"state": False, "error_message": error_message})
    else:
        return render(request, "chpwd.html")


def delete(request):
    User.objects.filter(username=request.session.get("username")).delete()  # 注销账号
    return render(request, "index.html", {"error_message": "账号注销成功！"})
def test(request):
    return render(request,'test.html')
def file_download(request):
    with open('static/pic/hello.txt') as f:
        c=f.read()
    return HttpResponse(c)
def big_file_download(request):
    def file_iterator(file_name,chunk_size=512):
        with open(file_name) as f:
            while True:
                c=f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    fname="static/pic/hello.jpeg"
    response=StreamingHttpResponse(file_iterator(fname))
    return response
def honeproc2(request):
    response=FileResponse(open('static/pic/0a0fc9492e3c3f2f9f3f85eca4095d00e558659f952bec52a87c991e7d806fcf.apk',"rb"))
    response['Content-Type']='application/octet-stream'#指定文件的类型
    response['Content-Disposition']='attachment;filename="{}.apk'.format("Dddd")#指定下载文件的默认名称
    print(type(response))
    return response


