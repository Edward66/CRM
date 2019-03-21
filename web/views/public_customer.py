from stark.service.version1 import StarkHandler, get_choice_text, get_m2m_text
from web.forms.public_customer import PublickCustomerModelForm


class PublicCustomerHandler(StarkHandler):
    list_display = ['name', 'contact_info', get_choice_text('状态', 'status'), get_m2m_text('咨询的课程', 'course')]

    def get_queryset(self, request, *args, **kwargs):
        return self.model_class.objects.filter(consultant__isnull=True)

    model_form_class = PublickCustomerModelForm
