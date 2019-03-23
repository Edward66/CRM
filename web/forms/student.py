from stark.service.version1 import StarkModelForm
from web import models


class StudentModelForm(StarkModelForm):
    class Meta:
        model = models.Student
        fields = ['qq', 'mobile', 'emergency_contact', 'memo']
