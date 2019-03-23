from django.shortcuts import HttpResponse
from django.urls import re_path
from django.utils.safestring import mark_safe

from stark.service.version1 import StarkHandler, get_datetime_text
from web import models
from web.forms.course_record import CourseRecordModelForm


class CourseRecordHandler(StarkHandler):
    list_display = [StarkHandler.display_checkbox, 'class_object', 'day_num', 'teacher',
                    get_datetime_text('时间', 'date')]
    model_form_class = CourseRecordModelForm

    def get_urls(self):
        patterns = [
            re_path(r'^list/(?P<class_id>\d+)/$', self.wrapper(self.list_view), name=self.get_list_url_name),
            re_path(r'^add/(?P<class_id>\d+)/$', self.wrapper(self.add_view), name=self.get_add_url_name),
            re_path(r'^edit/(?P<class_id>\d+)/(?P<pk>\d+)/$', self.wrapper(self.edit_view),
                    name=self.get_edit_url_name),
            re_path(r'^delete/(?P<class_id>\d+)/(?P<pk>\d+)/$', self.wrapper(self.delete_view),
                    name=self.get_delete_url_name),
        ]
        patterns.extend(self.extra_urls())
        return patterns

    def get_queryset(self, request, *args, **kwargs):
        class_id = kwargs.get('class_id')
        return self.model_class.objects.filter(class_object_id=class_id)

    def save(self, request, form, is_update, *args, **kwargs):
        class_id = kwargs.get('class_id')
        if not is_update:
            form.instance.class_object_id = class_id
        form.save()

    def display_edit_del(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return '操作'
        class_id = kwargs.get('class_id')
        tpl = '<a href="%s">编辑</a> <a href="%s">删除</a>' % (
            self.reverse_edit_url(class_id=class_id, pk=obj.pk, ),
            self.reverse_delete_url(class_id=class_id, pk=obj.pk, ))
        return mark_safe(tpl)

    def action_multi_init(self, request, *args, **kwargs):
        course_record_id_list = request.POST.getlist('pk')
        class_id = kwargs.get('class_id')

        class_obj = models.ClassList.objects.filter(id=class_id).first()
        if not class_obj:
            HttpResponse('班级不存在')
        # 班级里所有学生列表
        student_object_list = class_obj.student_set.all()

        for course_record_id in course_record_id_list:
            # 判断上课记录是否合法，防止不法分子篡改上课记录的id
            course_record_object = models.CourseRecord.objects.filter(id=course_record_id,
                                                                      class_object_id=class_id).first()
            if not course_record_object:
                continue

            # 判断此上课记录的考勤记录是否已经存在
            study_record_exists = models.StudyRecord.objects.filter(course_record=course_record_object).exists()
            if study_record_exists:
                continue

            # # 为每个学生在该天创建考勤记录
            # for stu in student_object_list:
            #     models.StudyRecord.objects.create(student_id=stu.id, course_record_id=course_record_id)

            # 只创建对象，没有在数据库提交
            study_record_object_list = [models.StudyRecord(student_id=stu.id, course_record_id=course_record_id) for stu
                                        in student_object_list]
            # 在数据库创建
            models.StudyRecord.objects.bulk_create(study_record_object_list, batch_size=50)

    action_multi_init.text = '批量初始化考勤'
    action_list = [action_multi_init, ]
