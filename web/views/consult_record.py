from django.urls import re_path

from stark.service.version1 import StarkHandler


class ConsultRecordHandler(StarkHandler):
    list_display = ['note', 'consultant', 'date']
    list_template = 'consult_record.html'

    def get_urls(self):
        patterns = [
            re_path(r'^list/(?P<customer_id>\d+)/$', self.wrapper(self.list_view), name=self.get_list_url_name),
            re_path(r'^add/$', self.wrapper(self.add_view), name=self.get_add_url_name),
            re_path(r'^edit/(?P<pk>\d+)/$', self.wrapper(self.edit_view), name=self.get_edit_url_name),
            re_path(r'^delete/(?P<pk>\d+)/$', self.wrapper(self.delete_view), name=self.get_delete_url_name),
        ]
        patterns.extend(self.extra_urls())
        return patterns

    def get_queryset(self, request, *args, **kwargs):
        customer_id = kwargs.get('customer_id')
        current_user_id = request.session['user_info']['id']
        return self.model_class.objects.filter(customer_id=customer_id, customer__consultant_id=current_user_id)
