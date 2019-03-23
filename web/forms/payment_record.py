from django import forms

from stark.service.version1 import StarkModelForm
from web import models


class PaymentRecordModelForm(StarkModelForm):
    class Meta:
        model = models.PaymentRecord
        fields = ['pay_type', 'paid_fee', 'class_list', 'note', ]


class StudentPaymentRecordModelForm(StarkModelForm):
    qq = forms.CharField(label='qq号', max_length=32)
    mobile = forms.CharField(label='手机号', max_length=32)
    emergency_contact = forms.CharField(label='紧急联系人', max_length=32)

    class Meta:
        model = models.PaymentRecord
        fields = ['pay_type', 'paid_fee', 'class_list', 'qq', 'mobile', 'emergency_contact', 'note', ]
