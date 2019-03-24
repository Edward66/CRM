from stark.service.version1 import StarkModelForm
from web import models


class StudyRecordModelForm(StarkModelForm):
    class Meta:
        model = models.StudyRecord
        fields = ['record', ]
