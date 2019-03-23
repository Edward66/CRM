from django.utils.safestring import mark_safe
from django.urls import reverse

from stark.service.version1 import (
    StarkHandler, get_datetime_text,
    get_m2m_text, Option
)
from web.forms.class_list import ClassListModelForm


class ClassListHandler(StarkHandler):
    def display_course(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return '班级'
        return '%s %s期' % (obj.course.title, obj.semester)

    def display_course_record(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return '上课记录'
        record_url = reverse('stark:web_courserecord_list', kwargs={'class_id': obj.pk})
        return mark_safe('<a target="_blank" href="%s">上课记录</a>' % record_url)

    list_display = ['school',
                    display_course,
                    'price',
                    get_datetime_text('开班日期', 'start_date', ),
                    'tutor',
                    get_m2m_text('任课老师', 'tech_teacher'),
                    display_course_record,
                    ]

    model_form_class = ClassListModelForm

    search_group = [
        Option('school', is_multi=True),
        Option('course', is_multi=True),
    ]
