from django.http import QueryDict

from django.shortcuts import reverse


def memory_url(request, name, *args, **kwargs):
    """
     生成带有原搜索条件的URL（替代了模板中的url）
    :param request:
    :param args:
    :param kwargs:
    :return:
    """

    # reverse用法：reverse('name', kwargs={'pk': 1})
    # reverse用法：reverse('name', args=(1,))
    basic_url = reverse(name, args=args, kwargs=kwargs)
    # 当前url中无参数
    if not request.GET:
        return basic_url

    old_params = request.GET.urlencode()  # 获取url中的参数

    query_dict = QueryDict(mutable=True)  # 提供转义功能
    query_dict['_filter'] = old_params

    # urlencode帮我们自动转义。
    # 如果不用urlencode，&符号会把这个参数分割成两个参数:_filter=mid=2 和 age=99
    return '%s?%s' % (basic_url, query_dict.urlencode())  # _filter=mid=2&age=99


def memory_reverse(request, name, *args, **kwargs):
    """
    反向生成URL
        http://127.0.0.1:8000/rbac/menu/edit/1/?_filter=mid%3D4
        1. 在URL获取原来的搜索条件获取（filter后的值）
        2. reverse生成原来的URL，如：/menu/list/
        3. /menu/list/?mid%3D4

    :param request:
    :param name:
    :param args:
    :param kwargs:
    :return:
    """

    url = reverse(name, args=args, kwargs=kwargs)
    original_parmas = request.GET.get('_filter')
    if original_parmas:
        url = '%s?%s' % (url, original_parmas)
    return url
