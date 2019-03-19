from stark.service.version1 import site, StarkHandler
from web import models


class SchoolHandler(StarkHandler):
    list_display = ['title', ]


class DepartmentHandler(StarkHandler):
    list_display = ['title']


site.register(models.School, SchoolHandler)
site.register(models.Department, DepartmentHandler)
