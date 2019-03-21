from django.utils.safestring import mark_safe
from django.urls import re_path
from django.shortcuts import render

from stark.service.version1 import StarkHandler, get_choice_text, get_m2m_text
from web.forms.public_customer import PublickCustomerModelForm
from web import models


class PublicCustomerHandler(StarkHandler):
    def display_record(self, obj=None, is_header=None):
        if is_header:
            return '跟进记录'
        record_url = self.reverse_commons_url(self.get_url_name('record_list'), pk=obj.pk)
        return mark_safe('<a href="%s">查看跟进</a>' % record_url)

    list_display = ['name', 'contact_info', display_record, get_choice_text('状态', 'status'),
                    get_m2m_text('咨询的课程', 'course')]

    def get_queryset(self, request, *args, **kwargs):
        return self.model_class.objects.filter(consultant__isnull=True)

    model_form_class = PublickCustomerModelForm

    def extra_urls(self):
        patterns = [
            re_path(r'^record/(?P<pk>\d+)/$', self.wrapper(self.record_view), name=self.get_url_name('record_list'))
        ]
        return patterns

    def record_view(self, request, pk):
        """
        查看跟进记录的视图
        :param request:
        :param pk:
        :return:
        """
        record_list = models.ConsultRecord.objects.filter(customer_id=pk)
        context = {
            'record_list': record_list,
        }
        return render(request, 'record_list.html', context)
