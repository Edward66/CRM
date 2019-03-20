from django import forms

from stark.service.version1 import StarkForm, StarkModelForm
from web import models
from web.utils.md5 import gen_md5


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


class ResetPasswordForm(StarkForm):
    password = forms.CharField(label='密码', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError('两次密码不一致')
            return confirm_password

    def clean(self):
        password = self.cleaned_data['password']
        self.cleaned_data['password'] = gen_md5(password)
        return self.cleaned_data
