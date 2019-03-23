from django.urls import re_path

from stark.service.version1 import StarkHandler, Option, get_choice_text, get_m2m_text
from web.forms.student import StudentModelForm


class StudentHandler(StarkHandler):
    list_display = ['customer', 'qq', 'mobile', 'emergency_contact', get_m2m_text('已报班级', 'class_list', ),
                    get_choice_text('学员状态', 'student_status')]

    model_form_class = StudentModelForm

    def get_add_btn(self, request, *args, **kwargs):
        return None

    def get_list_display(self):
        values = []
        if self.list_display:
            values.extend(self.list_display)
            values.append(type(self).display_edit)

        return values

    def get_urls(self):
        patterns = [
            re_path(r'^list/$', self.wrapper(self.list_view), name=self.get_list_url_name),
            re_path(r'^edit/(?P<pk>\d+)/$', self.wrapper(self.edit_view), name=self.get_edit_url_name),
        ]
        patterns.extend(self.extra_urls())  # 先去传进来的handler里找
        return patterns

    search_list = ['customer__name', 'qq', 'mobile']
    search_group = [
        Option('class_list', text_func=lambda x: '%s-%s' % (x.school.title, str(x)))
    ]
