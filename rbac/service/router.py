import re

from collections import OrderedDict

from django.conf import settings
from django.utils.module_loading import import_string  # 根据字符串的形式，帮我们去导入模块
from django.urls import URLPattern, URLResolver  # 路由分发：URLResolver。非路由分发：URLPattern


def check_url_exclude(url):
    """
    排除一些特定的url
    :param url:
    :return:
    """
    for regex in settings.AUTO_DISCOVER_EXCLUDE:
        if re.match(regex, url):
            return True


def recursion_urls(pre_namespace, pre_url, urlpatterns, url_ordered_dict):
    """
    :param pre_namespace: namespace前缀（rbac:xxx)，以后用于拼接name
    :param per_url: url的前缀（rbac/xxx）,以后用于拼接url
    :param urlpatterns: 路由关系列表
    :param url_ordered_dict: 用于保存递归中获取的所有路由
    :return:
    """

    # 路由分发：URLResolver。非路由分发：URLPattern
    for item in urlpatterns:
        if isinstance(item, URLPattern):  # 非路由分发，将路由添加到url_ordered_dict
            if not item.name:  # url中反向命名的name，没有的话不做处理，直接跳过。
                continue
            if pre_namespace:  # 如果有命名空间就进行拼接。示例：rbac:role_list
                name = f'{pre_namespace}:{item.name}'
            else:
                name = item.name  # 示例：role_list

            # 判断url有没有前缀，如果有前缀的话我们要给它拼接上，一般url都是有前缀的，因为从根级路由开始我们就加了个/
            url = pre_url + item.pattern.regex.pattern  # pattern.regex.pattern是拿到当前url django 1.X里是 url._regex
            # 拼接完长这样：/^rbac/^user/edit/(?P<pk>\d_+)/$
            url = url.replace('^', '').replace('$', '')  # 把起始符和终止符替换成空的，最后得到:/rbac/user/edit/(?P<pk>\d_+)/

            if check_url_exclude(url):  # 判断是否admin、login等我们不需要的url，是的话直接跳过
                continue

            url_ordered_dict[name] = {'name': name, 'url': url}
            # 'rbac:menu_list':{name:'rbac:menu_list',url:'xxxxx/yyyy/menu/list'}

        elif isinstance(item, URLResolver):  # 路由分发，进行递归操作
            if pre_namespace:
                """
                # 有前缀  示例：admin 。admin.site.urls的urls的返回值是：
                @property
                def urls(self):
                    return self.get_urls(), 'admin', self.name  。 返回值的第二个是命名空间
                """
                if item.namespace:  # 如果有自己的namespace比如说user_list,和前面的pre_namespace进行拼接，结果是rbac:user_list
                    namespace = f"{pre_namespace}:{item.namespace}"
                else:
                    """
                    自己没有namespace，但是父级有，那么namespace就应该是父级的，所以那就直接应该是rbac。
                    示例：re_path(r'^role/list/$', include('xxx.urls'))。rbac里的一条路由又进行路由分发，但是自己没有命名空间
                    """
                    namespace = item.namespace  # 写成namespace = pre_namespace也可以
            else:
                if item.namespace:  # 父级没有namespace，自己有。示例：re_path(r'^rbac/', include(('rbac.urls', 'rbac')), )
                    namespace = item.namespace
                else:  # 父级没有namespace，自己也没有
                    namespace = None

            recursion_urls(namespace, pre_url + item.pattern.regex.pattern, item.url_patterns, url_ordered_dict)

            """
            pre_url（上一级的url） + item.pattern.regex.pattern（当前路由分发的前缀）,item.url_patterns（当前路由分发的urlpatterns）
            拿re_path(r'^rbac/', include(('rbac.urls', 'rbac')))举例：
            namespace = rbac,  pre_url=/,  item.pattern.regex.pattern=^rbac/，item.url_patterns = rbac.urls下的所有url
            在django1.x里item.pattern.regex.pattern要换成item.regex.pattern
            """


def get_all_url_dict():
    """
    获取项目中所有的URL（必须有name别名）
    :return:
    """

    url_ordered_dict = OrderedDict()

    all_url = import_string(settings.ROOT_URLCONF)  # from permission_learn import urls

    recursion_urls(None, '/', all_url.urlpatterns, url_ordered_dict)  # 递归的去获取所有的路由。根目录没有namespace，根路由用/

    # 得到类似这样的结果：
    """
    {
        'rbac:menu_list':{name:'rbac:menu_list',url:'xxxxx/yyyy/menu/list'}
    }
    """

    return url_ordered_dict
