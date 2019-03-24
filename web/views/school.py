from stark.service.version1 import StarkHandler
from web.views.base import PermissionHanlder


class SchoolHandler(PermissionHanlder, StarkHandler):
    list_display = ['title', ]
