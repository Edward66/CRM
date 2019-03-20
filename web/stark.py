from stark.service.version1 import site
from web import models
from web.views.course import CourseHandler
from web.views.department import DepartmentHandler
from web.views.school import SchoolHandler
from web.views.userinfo import UserInfoHandler

site.register(models.School, SchoolHandler)
site.register(models.Department, DepartmentHandler)
site.register(models.UserInfo, UserInfoHandler)
site.register(models.Course, CourseHandler)
