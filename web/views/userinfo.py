from django.urls import re_path
from django.utils.safestring import mark_safe
from django.shortcuts import HttpResponse, render, redirect

from stark.service.version1 import StarkHandler, get_choice_text, Option
from web import models
from web.forms.userinfo import UserInfoAddModelForm, UserInfoEditModelForm, ResetPasswordForm


class UserInfoHandler(StarkHandler):
    def display_reset_pwd(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return '重置密码'
        reset_url = self.reverse_commons_url(self.get_url_name('reset_pwd'), pk=obj.pk)
        return mark_safe('<a href="%s">重置密码</a>' % reset_url)

    list_display = ['realname', get_choice_text('性别', 'gender'), 'phone', 'email', 'department', display_reset_pwd]
    search_list = ['name__contains', 'realname__contains']
    search_group = [
        Option(field='gender', is_multi=True),
        Option(field='department', is_multi=True),
    ]

    # 这个的优先级要大于其父类的
    def get_model_form_class(self, is_add=False):
        if is_add:
            return UserInfoAddModelForm
        else:
            return UserInfoEditModelForm

    def reset_password(self, request, pk):
        """
        密码的视图函数
        :param request:
        :param pk:
        :return:
        """
        userinfo_obj = models.UserInfo.objects.filter(id=pk).first()
        if not userinfo_obj:
            return HttpResponse('用户不存在，无法进行密码重置!')
        if request.method == 'GET':
            form = ResetPasswordForm()
            return render(request, 'stark/change.html', {'form': form})
        form = ResetPasswordForm(data=request.POST)
        if form.is_valid():
            # 密码更新到数据库
            userinfo_obj.password = form.cleaned_data['password']
            userinfo_obj.save()
            return redirect(self.reverse_list_url())
        return render(request, 'stark/change.html', {'form': form})

    def extra_urls(self):
        patterns = [
            re_path(r'^reset/password/(?P<pk>\d+)/$', self.wrapper(self.reset_password),
                    name=self.get_url_name('reset_pwd')),
        ]
        return patterns
