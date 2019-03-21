from stark.service.version1 import StarkHandler, get_choice_text, get_m2m_text
from web.forms.private_customer import PrivateCustomerModelForm


class PrivateCustomerHandler(StarkHandler):
    model_form_class = PrivateCustomerModelForm
    list_display = [StarkHandler.display_checkbox, 'name', 'contact_info',
                    get_choice_text('状态', 'status'),
                    get_m2m_text('咨询的课程', 'course')]

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
