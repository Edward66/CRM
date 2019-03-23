from django.urls import re_path
from stark.service.version1 import StarkHandler, get_choice_text


class PaymentRecordHandler(StarkHandler):
    """
    缴费记录不允许编辑和删除
    """
    list_display = [get_choice_text('缴费类型', 'pay_type'), 'paid_fee', 'class_list', 'consultant',
                    get_choice_text('状态', 'confirm_status')]

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
