from stark.service.version1 import site, StarkHandler, get_choice_text, StarkModelForm
from web import models


class SchoolHandler(StarkHandler):
    list_display = ['title', ]


class DepartmentHandler(StarkHandler):
    list_display = ['title']


class UserInfoModelForm(StarkModelForm):
    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'realname', 'gender', 'phone', 'email', 'department', 'roles']


class UserInfoHandler(StarkHandler):
    list_display = ['realname', get_choice_text('性别', 'gender'), 'phone', 'email', 'department']
    model_form_class = UserInfoModelForm


site.register(models.School, SchoolHandler)
site.register(models.Department, DepartmentHandler)
site.register(models.UserInfo, UserInfoHandler)
