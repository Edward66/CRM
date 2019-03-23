from stark.service.version1 import StarkModelForm
from web import models


class ScoreRecordModelForm(StarkModelForm):
    class Meta:
        model = models.ScoreRecord
        fields = ['content', 'score']
