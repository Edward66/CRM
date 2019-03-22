from django.db import transaction
from django.utils.safestring import mark_safe
from django.urls import re_path
from django.shortcuts import HttpResponse, render

from stark.service.version1 import StarkHandler, get_choice_text, get_m2m_text, Option
from web.forms.public_customer import PublickCustomerModelForm
from web import models


class PublicCustomerHandler(StarkHandler):
    def display_record(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return '跟进记录'
        record_url = self.reverse_commons_url(self.get_url_name('record_list'), pk=obj.pk)
        return mark_safe('<a href="%s">查看跟进</a>' % record_url)

    list_display = [StarkHandler.display_checkbox, 'name', 'contact_info', display_record,
                    get_choice_text('状态', 'status'),
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

    def action_multi_apply(self, request, *args, **kwargs):
        """
        批量申请到私户
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        """
        基本实现
        current_user_id = 6  # 暂时写死，等用上权限组件的时候要改成当前登录用户
        pk_list = request.POST.getlist('pk')

        # 将选中的客户更新到我的私户（consultant=当前自己）

        models.Customer.objects.filter(id__in=pk_list, status=2, consultant__isnull=True).update(
            consultant_id=current_user_id)
        """

        current_user_id = request.session['user_info']['id']
        pk_list = request.POST.getlist('pk')
        UN_SIGN_UP = 2
        private_customer_count = models.Customer.objects.filter(consultant_id=current_user_id,
                                                                status=UN_SIGN_UP).count()

        # 私户个数限制
        if private_customer_count + len(pk_list) > models.Customer.MAX_PRIVATE_CUSTOMER_COUNT:
            return HttpResponse(
                f'做人不要太贪心，私户中已有{private_customer_count}个客户，最多只能申请{models.Customer.MAX_PRIVATE_CUSTOMER_COUNT - private_customer_count}')

        # 数据库中加锁

        apply_success = False
        with transaction.atomic():  # 事物
            # 在数据库中加锁
            original_queryset = models.Customer.objects.filter(id__in=pk_list, status=UN_SIGN_UP,
                                                               consultant__isnull=True).select_for_update()
            if len(original_queryset) == len(pk_list):  # 如果不相等，可能就有数据被别人申请走了
                models.Customer.objects.filter(id__in=pk_list, status=UN_SIGN_UP,
                                               consultant__isnull=True).update(consultant_id=current_user_id)
                apply_success = True
            if not apply_success:
                return HttpResponse('手速太慢了，选中的客户已被其他人申请，请重新选择')

    action_multi_apply.text = '申请到我的私户'

    action_list = [action_multi_apply, ]

    search_list = ['name__contains', ]

    search_group = [
        Option(field='gender', is_multi=True),
        Option(field='status', is_multi=True),
        Option(field='course', is_multi=True),
        Option(field='education', is_multi=True),
    ]
