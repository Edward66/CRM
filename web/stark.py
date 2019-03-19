from django import forms

from stark.service.version1 import site, StarkHandler, get_choice_text, StarkModelForm
from web import models
from web.utils.md5 import gen_md5


class SchoolHandler(StarkHandler):
    list_display = ['title', ]


class DepartmentHandler(StarkHandler):
    list_display = ['title']


class UserInfoAddModelForm(StarkModelForm):
    confirm_password = forms.CharField(
        label='确认密码'
    )

    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'confirm_password', 'realname', 'gender', 'phone', 'email', 'department', 'roles']

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError('密码输入不一致')
        return confirm_password

    def clean(self):
        password = self.cleaned_data['password']
        self.cleaned_data['password'] = gen_md5(password)
        return self.cleaned_data


class UserInfoEditModelForm(StarkModelForm):
    class Meta:
        model = models.UserInfo
        fields = ['name', 'realname', 'gender', 'phone', 'email', 'department', 'roles']


class UserInfoHandler(StarkHandler):
    list_display = ['realname', get_choice_text('性别', 'gender'), 'phone', 'email', 'department']

    # 这个的优先级要大于其父类的
    def get_model_form_class(self, is_add=False):
        if is_add:
            return UserInfoAddModelForm
        else:
            return UserInfoEditModelForm


site.register(models.School, SchoolHandler)
site.register(models.Department, DepartmentHandler)
site.register(models.UserInfo, UserInfoHandler)
