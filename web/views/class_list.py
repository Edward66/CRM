from stark.service.version1 import StarkHandler, get_datetime_text, get_m2m_text


class ClassListHandler(StarkHandler):
    def display_course(self, obj=None, is_header=None):
        if is_header:
            return '班级'
        return '%s %s期' % (obj.course.title, obj.semester)

    list_display = ['school', display_course, 'price', get_datetime_text('开班日期', 'start_date', ), 'tutor',
                    get_m2m_text('任课老师', 'tech_teacher')]
