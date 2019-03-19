from django.conf import settings


def init_permission(current_user, request):
    """
    用户权限的初始化
    :param current_user:  当前登录用户
    :param request:
    :return:
    """

    permission_menu_queryset = current_user.roles.filter(permissions__isnull=False).values(
        'permissions__id',
        'permissions__title',
        'permissions__url',
        'permissions__name',
        'permissions__pid_id',
        'permissions__pid__title',  # +
        'permissions__pid__url',
        'permissions__menu_id',
        'permissions__menu__title',
        'permissions__menu__icon',
    )

    permission_dict = {}  # +

    menu_dict = {}

    for item in permission_menu_queryset:
        permission_dict[item['permissions__name']] = {
            'id': item['permissions__id'],
            'title': item['permissions__title'],
            'url': item['permissions__url'],
            'pid': item['permissions__pid_id'],
            'p_title': item['permissions__pid__title'],
            'p_url': item['permissions__pid__url'],
        }

        menu_id = item['permissions__menu_id']

        if not menu_id:
            continue

        second_menu = {'id': item["permissions__id"], 'title': item['permissions__title'],
                       'url': item['permissions__url']}

        if menu_id in menu_dict:
            menu_dict[menu_id]['second_menu'].append(second_menu)
        else:
            menu_dict[menu_id] = {
                'title': item['permissions__menu__title'],
                'icon': item['permissions__menu__icon'],
                'second_menu': [second_menu, ]
            }

    request.session[settings.PERMISSION_SESSION_KEY] = permission_dict
    request.session[settings.MENU_SESSION_KEY] = menu_dict
