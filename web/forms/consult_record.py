from stark.service.version1 import StarkModelForm
from web import models


class ConsuleRecordModelForm(StarkModelForm):
    class Meta:
        model = models.ConsultRecord
        fields = ['note',]
