"""
角色管理
"""

from django.shortcuts import HttpResponse, render, redirect, reverse

from rbac import models
from rbac.forms.roles import RoleModelForm


def role_list(request):
    """
       角色列表
       :param request:
       :return:
       """
    role_queryset = models.Role.objects.all()
    return render(request, 'rbac/role_list.html', {'role_list': role_queryset})


def role_add(request):
    """
    添加角色
    :param request:
    :return:
    """
    if request.method == 'GET':
        forms = RoleModelForm()
        return render(request, 'rbac/change.html', {'forms': forms})

    forms = RoleModelForm(data=request.POST)
    if forms.is_valid():
        forms.save()
        return redirect(reverse('rbac:role_list'))
    return render(request, 'rbac/change.html', {'forms': forms})


def role_edit(request, pk):
    """
    编辑角色
    :param request:
    :param pk: 要修改的角色id
    :return:
    """
    role_obj = models.Role.objects.filter(id=pk).first()

    if not role_obj:
        return HttpResponse('角色不存在')

    if request.method == 'GET':
        forms = RoleModelForm(instance=role_obj)
        return render(request, 'rbac/change.html', {'forms': forms})

    forms = RoleModelForm(data=request.POST, instance=role_obj)

    if forms.is_valid():
        forms.save()
        return redirect(reverse('rbac:role_list'))
    return render(request, 'rbac/change.html', {'forms': forms})


def role_del(request, pk):
    """
    删除角色
    :param request:
    :param pk:
    :return:
    """
    role_list_url = reverse('rbac:role_list')

    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': role_list_url})

    models.Role.objects.filter(id=pk).delete()
    return redirect(role_list_url)
