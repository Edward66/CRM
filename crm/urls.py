from django.conf.urls import re_path
from django.contrib import admin

from stark.service.version1 import site
from web.views import account

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'stark/', site.urls),
    re_path(r'^login/$', account.login, name='login'),
    re_path(r'^logout/$', account.logout, name='logout'),
    re_path(r'^index/$', account.index, name='index'),
]
