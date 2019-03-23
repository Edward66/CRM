from django.urls import re_path

from stark.service.version1 import StarkHandler, get_choice_text, get_datetime_text


class CheckPaymentRecord(StarkHandler):
    order_list = ['-id', 'confirm_status']

    # TODO:customer换成这个客户的真名和真实联系方式（在Student表中）
    list_display = [StarkHandler.display_checkbox, 'customer', get_choice_text('缴费类型', 'pay_type'), 'paid_fee',
                    'class_list',
                    get_datetime_text('申请日期', 'apply_date'),
                    get_choice_text('审核状态', 'confirm_status'),
                    'consultant', ]

    def get_list_display(self):
        """
        获取页面上应该显示的列,自定义扩展，列如：根据用户的不同来显示不同的列
        :return:
        """
        values = []
        if self.list_display:
            values.extend(self.list_display)
            # 默认显示编辑和删除
            # type(self) 当前对象的类
        return values

    def get_add_btn(self, request, *args, **kwargs):
        return None

    def get_urls(self):  # 先在传进来的handler里重写
        patterns = [
            re_path(r'^list/$', self.wrapper(self.list_view), name=self.get_list_url_name),
        ]
        patterns.extend(self.extra_urls())  # 先去传进来的handler里找
        return patterns

    def action_multi_confirm(self, request, *args, **kwargs):
        """
        批量确认
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 已确认或已驳回后台是不会做任何操作的
        pk_list = request.POST.getlist('pk')
        # 缴费记录
        # 客户表
        # 学生表
        applying = 1  # 申请中
        confirm = 2  # 已确认
        sign_up = 1  # 已报名
        learning = 2  # 在读

        for pk in pk_list:
            # 必须是申请中的状态才能确认
            payment_object = self.model_class.objects.filter(id=pk, confirm_status=applying).first()
            if not payment_object:
                continue
            payment_object.confirm_status = confirm
            payment_object.save()

            payment_object.customer.status = sign_up
            payment_object.customer.save()

            payment_object.customer.student.student_status = learning
            payment_object.customer.student.save()

    action_multi_confirm.text = '批量确认'

    def action_multi_cancel(self, request, *args, **kwargs):
        """
        批量驳回操作
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 已确认或已驳回后台是不会做任何操作的
        pk_list = request.POST.getlist('pk')
        applying = 1
        reject = 3
        # 必须是申请中的状态才可以驳回
        self.model_class.objects.filter(id__in=pk_list, confirm_status=applying).update(confirm_status=reject)

    action_multi_cancel.text = '批量驳回'

    action_list = [action_multi_confirm, action_multi_cancel]
