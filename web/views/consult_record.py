from django.shortcuts import HttpResponse
from django.urls import re_path
from django.utils.safestring import mark_safe

from stark.service.version1 import StarkHandler
from web import models
from web.forms.consult_record import ConsuleRecordModelForm


class ConsultRecordHandler(StarkHandler):
    list_display = ['note', 'consultant', 'date']
    list_template = 'consult_record.html'
    model_form_class = ConsuleRecordModelForm

    def get_urls(self):
        patterns = [
            re_path(r'^list/(?P<customer_id>\d+)/$', self.wrapper(self.list_view), name=self.get_list_url_name),
            re_path(r'^add/(?P<customer_id>\d+)/$', self.wrapper(self.add_view), name=self.get_add_url_name),
            re_path(r'^edit/(?P<customer_id>\d+)/(?P<pk>\d+)/$', self.wrapper(self.edit_view),
                    name=self.get_edit_url_name),
            re_path(r'^delete/(?P<customer_id>\d+)/(?P<pk>\d+)/$', self.wrapper(self.delete_view),
                    name=self.get_delete_url_name),
        ]
        patterns.extend(self.extra_urls())
        return patterns

    def get_queryset(self, request, *args, **kwargs):
        customer_id = kwargs.get('customer_id')
        current_user_id = request.session['user_info']['id']
        return self.model_class.objects.filter(customer_id=customer_id, customer__consultant_id=current_user_id)

    def save(self, request, form, is_update, *args, **kwargs):
        customer_id = kwargs.get('customer_id')
        current_user_id = request.session['user_info']['id']

        customer_object_exists = models.Customer.objects.filter(
            id=customer_id, consultant_id=current_user_id).exists()
        if not customer_object_exists:
            return HttpResponse('非法操作')
        if not is_update:
            form.instance.customer_id = customer_id
            form.instance.consultant_id = current_user_id
        form.save()

    # 源码中没有customer_id的参数
    def display_edit_del(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return '操作'
        customer_id = kwargs.get('customer_id')
        tpl = '<a href="%s">编辑</a> <a href="%s">删除</a>' % (
            self.reverse_edit_url(customer_id=customer_id, pk=obj.pk, ),
            self.reverse_delete_url(customer_id=customer_id, pk=obj.pk, ))
        return mark_safe(tpl)

    def get_edit_object(self, request, pk, *args, **kwargs):
        customer_id = kwargs.get('customer_id')
        current_user_id = request.session['user_info']['id']
        # 当前记录的客户的课程顾问必须是登录的课程顾问
        return models.ConsultRecord.objects.objects.filter(pk=pk, customer_id=customer_id,
                                                           customer__consultant_id=current_user_id).first()

    def get_delete_object(self, request, pk, *args, **kwargs):
        customer_id = kwargs.get('customer_id')
        current_user_id = request.session['user_info']['id']
        record_queryset = models.ConsultRecord.objects.objects.filter(pk=pk, customer_id=customer_id,
                                                                      customer__consultant_id=current_user_id)

        if not record_queryset.exists():
            return HttpResponse('要删除的记录不存在，请重新选择')
        record_queryset.delete()
