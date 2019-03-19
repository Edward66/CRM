import re
from collections import OrderedDict

from django.conf import settings
from django.template import Library

from rbac.service import urls

register = Library()


@register.inclusion_tag('rbac/menu.html')
def menu(request):
    """
    创建一级菜单
    :param request:
    :return:
    """
    menu_list = request.session[settings.MENU_SESSION_KEY]
    current_path = request.path

    for item in menu_list:
        reg = '^%s$' % item['url']
        if re.match(reg, current_path):
            item['class'] = 'active'

    # menu函数里面的返回值是返回到 rbac/templates/rbac/menu.html
    # menu函数里面的返回值也可以说是返回到inclusion_tag所指向的模版路径
    context = {
        'menu_list': menu_list,
        'current_path': current_path
    }

    return context


@register.inclusion_tag('rbac/multi_menu.html')
def multi_menu(request):
    menu_dict = request.session[settings.MENU_SESSION_KEY]

    key_list = sorted(menu_dict)

    ordered_dict = OrderedDict()

    for key in key_list:
        menu = menu_dict[key]
        menu['class'] = 'hide'

        for second_menu in menu['second_menu']:
            if second_menu['id'] == request.current_selected_permission:
                second_menu['class'] = 'active'
                menu['class'] = ''

        ordered_dict[key] = menu

    context = {
        'menus': ordered_dict
    }

    return context


@register.inclusion_tag('rbac/breadcrumb.html')
def breadcrumb(request):
    return {'record_list': request.breadcrumb}


@register.filter()
def has_permission(request, name):
    """判断是否有权限"""

    if name in request.session[settings.PERMISSION_SESSION_KEY]:
        return True


@register.simple_tag()
def memory_url(request, name, *args, **kwargs):
    """
    生成带有原搜索条件的URL（替代了模板中的url）
    :param request:
    :param name:
    :param args:
    :param kwargs:
    :return:
    """
    return urls.memory_url(request, name, *args, **kwargs)
