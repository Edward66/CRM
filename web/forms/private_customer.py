from stark.service.version1 import StarkModelForm
from web import models


class PrivateCustomerModelForm(StarkModelForm):
    class Meta:
        model = models.Customer
        exclude = ['consultant']
