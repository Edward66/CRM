from django.urls import re_path

from stark.service.version1 import StarkHandler
from web.forms.score_record import ScoreRecordModelForm


class ScoreHandler(StarkHandler):
    list_display = ['content', 'score', 'user', ]
    model_form_class = ScoreRecordModelForm

    def get_urls(self):  # 先在传进来的handler里重写
        patterns = [
            re_path(r'^list/(?P<student_id>\d+)/$', self.wrapper(self.list_view), name=self.get_list_url_name),
            re_path(r'^add/(?P<student_id>\d+)/$', self.wrapper(self.add_view), name=self.get_add_url_name),
        ]
        patterns.extend(self.extra_urls())
        return patterns

    def get_list_display(self):
        values = []
        if self.list_display:
            values.extend(self.list_display)
        return values

    def get_queryset(self, request, *args, **kwargs):
        student_id = kwargs.get('student_id')
        return self.model_class.objects.filter(student_id=student_id)

    def save(self, request, form, is_update, *args, **kwargs):
        student_id = kwargs.get('student_id')
        current_user_id = request.session['user_info']['id']

        form.instance.student_id = student_id
        form.instance.user_id = current_user_id
        form.save()

        # 原积分
        alter_score = form.instance.score
        if alter_score > 0:
            form.instance.student.score += abs(alter_score)
        else:
            form.instance.student.score -= abs(alter_score)

        form.instance.student.save()
