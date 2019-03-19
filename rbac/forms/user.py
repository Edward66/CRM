from django import forms

from rbac import models

from .base import BaseBootStrapForm


class UserModelForm(BaseBootStrapForm):
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'confirm_password', 'email']

        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError('两次密码输入不一致')
            else:
                return confirm_password


class UpdateUserModelForm(BaseBootStrapForm):
    class Meta:
        model = models.UserInfo
        fields = ['name', 'email']


class ResetPwdUserModelForm(BaseBootStrapForm):
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = models.UserInfo
        fields = ['password', 'confirm_password']

        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_confirm_password(self):
        """检测两次面是否一致"""

        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError('两次密码不一致')
            else:
                return confirm_password
