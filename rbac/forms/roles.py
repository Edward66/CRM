from django import forms

from rbac import models
from rbac.forms.base import BaseBootStrapForm


class RoleModelForm(BaseBootStrapForm):
    class Meta:
        model = models.Role
        fields = ['title', ]
