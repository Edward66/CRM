from stark.service.version1 import StarkModelForm
from stark.forms.widgets import DateTimePickerInput
from web import models


class ClassListModelForm(StarkModelForm):
    class Meta:
        model = models.ClassList
        fields = '__all__'
        widgets = {
            'start_date': DateTimePickerInput,
            'graduate_date': DateTimePickerInput,
        }
