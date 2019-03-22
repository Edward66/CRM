from django.utils.safestring import mark_safe
from django.urls import reverse

from stark.service.version1 import StarkHandler, get_choice_text, get_m2m_text
from web.forms.private_customer import PrivateCustomerModelForm


class PrivateCustomerHandler(StarkHandler):
    model_form_class = PrivateCustomerModelForm

    def display_record(self, obj=None, is_header=None,*args,**kwargs):
        if is_header:
            return '跟进记录'
        # 这个用不着加原搜索条件,加了也用不上。到跟进记录页面后，增删改后没必要返回到私户页面，而是返回跟进记录的列表页面
        # 跳转到记录页面，url要自己写，self.get_url_name('xx')生成的都是customer的url
        record_url = reverse('stark:web_consultrecord_list', kwargs={'customer_id': obj.id})
        return mark_safe('<a target="_blank" href="%s">查看跟进</a>' % record_url)

    list_display = [StarkHandler.display_checkbox, 'name', 'contact_info',
                    get_choice_text('状态', 'status'),
                    get_m2m_text('咨询的课程', 'course'),
                    display_record, ]

    def get_queryset(self, request, *args, **kwargs):
        current_user_id = request.session['user_info']['id']
        return self.model_class.objects.filter(consultant_id=current_user_id)

    def save(self, request, form, is_update, *args, **kwargs):
        if not is_update:
            current_user_id = request.session['user_info']['id']
            form.instance.consultant_id = current_user_id
        form.save()

    def action_multi_transfer(self, request, *args, **kwargs):
        """
        批量移除到公户
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        current_user_id = request.session['user_info']['id']
        pk_list = request.POST.getlist('pk')
        self.model_class.objects.filter(id__in=pk_list, consultant_id=current_user_id).update(
            consultant=None
        )

    action_multi_transfer.text = '移除到公户'

    action_list = [action_multi_transfer, ]
