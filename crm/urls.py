from django.conf.urls import re_path
from django.contrib import admin

from stark.service.version1 import site

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'stark/', site.urls)
]
