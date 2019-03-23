from stark.service.version1 import StarkModelForm
from web import models


class CourseRecordModelForm(StarkModelForm):
    class Meta:
        model = models.CourseRecord
        fields = ['day_num', 'teacher']
