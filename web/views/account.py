from django.shortcuts import redirect, render

from rbac.service.init_permission import init_permission
from web import models
from web.utils.md5 import gen_md5


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    username = request.POST.get('username')
    password = gen_md5(request.POST.get('password', ''))

    user = models.UserInfo.objects.filter(name=username, password=password).first()
    if not user:
        return render(request, 'login.html', {'msg': '用户名或错误'})

    request.session['user_info'] = {'id': user.id, 'nickname': user.realname}

    # 权限信息初始化
    init_permission(user, request)

    return redirect('/index/')


def logout(request):
    request.session.flush()
    return redirect('/login/')


def index(request):
    return render(request, 'index.html')
