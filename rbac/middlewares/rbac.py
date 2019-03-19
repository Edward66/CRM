import re

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
from django.conf import settings


class RbacMiddleware(MiddlewareMixin):
    def process_request(self, request):

        white_list = settings.WHITE_LIST

        current_path = request.path

        for valid_url in white_list:
            if re.match(valid_url, current_path):
                return None

        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)

        if not permission_dict:
            return HttpResponse('请先登录 ')

        url_record = [
            {'title': '首页', 'url': '#'}
        ]

        # 此处代码进行判断：/logout/,/index/  无需权限校验，但是需要登录才能访问
        for url in settings.NO_PERMISSION_LIST:
            if re.match(url, request.path_info):
                # 需要登录，但无需权限校验
                request.current_selected_permission = 0  # 等于0就是没有默认选中,和菜单没有关联上，就不会做默认展开
                request.breadcrumb = url_record
                return None

        has_permission = False

        for item in permission_dict.values():
            regex = '^%s$' % item['url']
            if re.match(regex, current_path):
                has_permission = True
                request.current_selected_permission = item['pid'] or item['id']
                if not item['pid']:  # 选中的是二级菜单
                    url_record.extend([
                        {'title': item['title'], 'url': item['url'], 'class': 'active'}
                    ])
                else:  # 选中的是具体权限
                    url_record.extend([
                        {'title': item['p_title'], 'url': item['p_url']},
                        {'title': item['title'], 'url': item['url'], 'class': 'active'},
                    ])
                request.breadcrumb = url_record  # 通过request，把储存信息传给用户
                break

        if not has_permission:
            return HttpResponse('未获取权限，请先获取权限')
