from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse

from rbac.forms.user import UserModelForm, UpdateUserModelForm, ResetPwdUserModelForm
from rbac import models


def user_list(request):
    user_queryset = models.UserInfo.objects.all()

    return render(request, 'rbac/user_list.html', {'user_list': user_queryset})


def user_add(request):
    if request.method == 'GET':
        forms = UserModelForm()
        return render(request, 'rbac/change.html', {'forms': forms})

    forms = UserModelForm(data=request.POST)
    if forms.is_valid():
        forms.save()
        return redirect(reverse('rbac:user_list'))

    return render(request, 'rbac/change.html', {'forms': forms})


def user_edit(request, pk):
    user_obj = models.UserInfo.objects.filter(id=pk).first()

    if request.method == 'GET':
        forms = UpdateUserModelForm(instance=user_obj)
        return render(request, 'rbac/change.html', {'forms': forms})

    forms = UpdateUserModelForm(data=request.POST, instance=user_obj)
    if forms.is_valid():
        forms.save()
        return redirect(reverse('rbac:user_list'))

    return render(request, 'rbac/change.html', {'forms': forms})


def user_del(request, pk):
    user_list_url = reverse('rbac:user_list')

    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': user_list_url})

    models.UserInfo.objects.filter(id=pk).delete()

    return redirect(user_list_url)


def user_reset_pwd(request, pk):
    user_obj = models.UserInfo.objects.filter(id=pk).first()

    if not user_obj:
        return HttpResponse('用户不存在')

    if request.method == 'GET':
        forms = ResetPwdUserModelForm()
        return render(request, 'rbac/change.html', {'forms': forms})

    forms = ResetPwdUserModelForm(data=request.POST, instance=user_obj)

    if forms.is_valid():
        forms.save()
        return redirect(reverse('rbac:user_list'))

    return render(request, 'rbac/change.html', {'forms': forms})
