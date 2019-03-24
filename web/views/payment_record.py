from django.shortcuts import HttpResponse
from django.urls import re_path

from stark.service.version1 import StarkHandler, get_choice_text
from web import models
from web.forms.payment_record import PaymentRecordModelForm, StudentPaymentRecordModelForm
from web.views.base import PermissionHanlder


class PaymentRecordHandler(PermissionHanlder, StarkHandler):
    """
    缴费记录不允许编辑和删除
    """
    list_display = [get_choice_text('缴费类型', 'pay_type'), 'paid_fee', 'class_list', 'consultant',
                    get_choice_text('状态', 'confirm_status')]

    def get_urls(self):
        # 在list_view循环list_display的时候会执行get_choice_text()方法，由于此list_view传了customer_id，
        # 在执行get_choice_text --> field_or_func(self, queryset_obj, False, *args, **kwargs)
        # 的时候会传给get_choice_text，所以get_choice_text里的wrapper函数要加上*args和**kwargs成为：
        #  def wrapper(self, obj=None, is_header=None, *args, **kwargs)
        patterns = [
            re_path(r'^list/(?P<customer_id>\d+)/$', self.wrapper(self.list_view), name=self.get_list_url_name),
            re_path(r'^add/(?P<customer_id>\d+)/$', self.wrapper(self.add_view), name=self.get_add_url_name),
        ]
        patterns.extend(self.extra_urls())
        return patterns

    def get_queryset(self, request, *args, **kwargs):
        customer_id = kwargs.get('customer_id')
        current_user_id = request.session['user_info']['id']
        return self.model_class.objects.filter(customer_id=customer_id, customer__consultant_id=current_user_id)

    def get_list_display(self, request, *args, **kwargs):
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

    def get_model_form_class(self, is_add, request, pk, *args, **kwargs):
        # add_view调用self.get_model_form_class()时会传递customer_id给它
        # 如果当前客户有学生信息,则使用PaymentRecordModelForm，否则则使用StudentPaymentRecordModelForm
        customer_id = kwargs.get('customer_id')
        student_exists = models.Student.objects.filter(customer_id=customer_id).exists()
        if not student_exists:
            return StudentPaymentRecordModelForm
        return PaymentRecordModelForm

    def save(self, request, form, is_update, *args, **kwargs):
        customer_id = kwargs.get('customer_id')
        current_user_id = request.session['user_info']['id']
        object_exists = models.Customer.objects.filter(id=customer_id, consultant_id=current_user_id).exists()

        if not object_exists:
            return HttpResponse('非法操作')

        form.instance.customer_id = customer_id
        form.instance.consultant_id = current_user_id
        # 创建缴费记录信息
        form.save()

        # 创建学员信息
        class_list = form.cleaned_data['class_list']
        student_exists = models.Student.objects.filter(customer_id=customer_id).first()
        if not student_exists:  # 没有学生信息，用户填了学生信息才走下面
            qq = form.cleaned_data['qq']
            mobile = form.cleaned_data['mobile']
            emergency_contact = form.cleaned_data['emergency_contact']

            student_object = models.Student.objects.create(customer_id=customer_id, qq=qq, mobile=mobile,
                                                           emergency_contact=emergency_contact)
            student_object.class_list.add(class_list.id)
        else:  # 对于存在的学员，想报另外一个班
            student_exists.class_list.add(class_list)  # class_list和class_list.id都可以
