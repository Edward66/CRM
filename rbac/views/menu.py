from collections import OrderedDict

from django.conf import settings
from django.forms import formset_factory
from django.shortcuts import HttpResponse, render, redirect, reverse
from django.utils.module_loading import import_string

from rbac import models
from rbac.forms.menu import (
    MenuModelForm, SecondMenuModelForm, PermissionModelForm,
    MultiAddPermissionForm, MultiEditPermissionForm
)
from rbac.service.urls import memory_reverse
from rbac.service.router import get_all_url_dict


def menu_list(request):
    """
    菜单和权限列表
    :param request:
    :return:
    """
    menu_queryset = models.Menu.objects.all()

    menu_id = request.GET.get('mid')  # 用户选择的一级菜单

    menus_exists = models.Menu.objects.filter(id=menu_id).exists()

    if not menus_exists:
        menu_id = None

    if menu_id:
        second_menus = models.Permission.objects.filter(menu_id=menu_id)
    else:
        second_menus = []

    second_menu_id = request.GET.get('sid')  # 用户选择的二级菜单

    second_menus_exists = models.Permission.objects.filter(id=second_menu_id).exists()

    if not second_menus_exists:
        second_menu_id = None

    if second_menu_id:
        permissions = models.Permission.objects.filter(pid__id=second_menu_id)
    else:
        permissions = []

    context = {
        'menu_list': menu_queryset,
        'menu_id': menu_id,
        'second_menus': second_menus,
        'second_menu_id': second_menu_id,
        'permissions': permissions
    }

    return render(request, 'rbac/menu_list.html', context)


def menu_add(request):
    """
     菜单和权限列表
    :param request:
    :return:
    """
    if request.method == 'GET':
        forms = MenuModelForm()
        return render(request, 'rbac/change.html', {'forms': forms})

    forms = MenuModelForm(data=request.POST)
    if forms.is_valid():
        forms.save()
        url = memory_reverse(request, 'rbac:menu_list')
        return redirect(url)

    return render(request, 'rbac/change.html', {'forms': forms})


def menu_edit(request, pk):
    """
    编辑一级菜单
    :param request:
    :param pk:
    :return:
    """
    menu_obj = models.Menu.objects.filter(id=pk).first()

    if not menu_obj:
        return HttpResponse('菜单不存在')

    if request.method == 'GET':
        forms = MenuModelForm(instance=menu_obj)
        return render(request, 'rbac/change.html', {'forms': forms})

    forms = MenuModelForm(data=request.POST, instance=menu_obj)
    if forms.is_valid():
        forms.save()
        url = memory_reverse(request, 'rbac:menu_list')
        return redirect(url)
    return render(request, 'rbac/change.html', {'forms': forms})


def menu_del(request, pk):
    """
    删除一级菜单
    :param request:
    :param pk:
    :return:
    """
    menu_list_url = memory_reverse(request, 'rbac:menu_list')

    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': menu_list_url})

    models.Menu.objects.filter(id=pk).delete()

    return redirect(menu_list_url)


# 二级菜单的增删改


def second_menu_add(request, menu_id):
    """
    增加二级菜单
    :param request:
    :param pk:  已经选择的一级菜单ID（用于设置默认值)
    :return:
    """
    menu_obj = models.Menu.objects.filter(id=menu_id).first()

    if request.method == 'GET':
        forms = SecondMenuModelForm(initial={'menu': menu_obj})
        return render(request, 'rbac/change.html', {'forms': forms})

    forms = SecondMenuModelForm(data=request.POST)
    if forms.is_valid():
        forms.save()
        url = memory_reverse(request, 'rbac:menu_list')
        return redirect(url)
    return render(request, 'rbac/change.html', {'forms': forms})


def second_menu_edit(request, pk):
    """
    编辑二级菜单
    :param request:
    :param pk:
    :return:
    """

    permission_obj = models.Permission.objects.filter(id=pk).first()

    if request.method == 'GET':
        forms = SecondMenuModelForm(instance=permission_obj)
        return render(request, 'rbac/change.html', {'forms': forms})

    forms = SecondMenuModelForm(data=request.POST, instance=permission_obj)
    if forms.is_valid():
        forms.save()
        url = memory_reverse(request, 'rbac:menu_list')
        return redirect(url)

    return render(request, 'rbac/change.html', {'forms': forms})


def second_menu_del(request, pk):
    """
    删除二级菜单
    :param request:
    :param pk:
    :return:
    """

    menu_list_url = memory_reverse(request, 'rbac:menu_list')

    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': menu_list_url})

    models.Permission.objects.filter(id=pk).delete()
    return redirect(menu_list_url)


# 权限的增删改

def permission_add(request, second_menu_id):
    """
    添加权限
    :param request:
    :param pk:
    :return:
    """

    if request.method == 'GET':
        forms = PermissionModelForm()
        return render(request, 'rbac/change.html', {'forms': forms})

    forms = PermissionModelForm(data=request.POST)
    if forms.is_valid():
        second_menu_obj = models.Permission.objects.filter(id=second_menu_id).first()
        if not second_menu_obj:
            return HttpResponse('二级菜单不存在,请重新选择')
        forms.instance.pid = second_menu_obj  # form.instance中包含用户提交的所有值
        forms.save()
        url = memory_reverse(request, 'rbac:menu_list')
        return redirect(url)
    return render(request, 'rbac/change.html', {'forms': forms})


def permission_edit(request, pk):
    """
    权限编辑
    :param request:
    :param pk: 要编辑的权限id
    :return:
    """
    permission_obj = models.Permission.objects.filter(id=pk).first()

    if request.method == 'GET':
        forms = PermissionModelForm(instance=permission_obj)
        return render(request, 'rbac/change.html', {'forms': forms})

    forms = PermissionModelForm(data=request.POST, instance=permission_obj)
    if forms.is_valid():
        forms.save()
        url = memory_reverse(request, 'rbac:menu_list')
        return redirect(url)
    return render(request, 'rbac/change.html', {'forms': forms})


def permission_del(request, pk):
    """
    权限删除
    :param request:
    :param pk:
    :return:
    """
    menu_list_url = memory_reverse(request, 'rbac:menu_list')

    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': menu_list_url})

    models.Permission.objects.filter(id=pk).delete()

    return redirect(menu_list_url)


def multi_permissions(request):
    """
    批量操作权限
    :param request:
    :return:
    """

    post_type = request.GET.get('type')

    generate_formset_class = formset_factory(MultiAddPermissionForm, extra=0)
    update_formset_class = formset_factory(MultiEditPermissionForm, extra=0)
    generate_formset = None  # 出错了赋值，为了返回给页面错误信息
    update_formset = None  # 出错了赋值，为了返回给页面错误信息

    # 批量添加
    if request.method == 'POST' and post_type == 'generate':
        formset = generate_formset_class(data=request.POST)  # 储存的所有信息，包括html标签
        if formset.is_valid():
            has_repeat_error = False
            permission_obj_list = []
            url_form_list = formset.cleaned_data
            for num in range(0, formset.total_form_count()):
                url_form = url_form_list[num]
                # 下面的方式和model.Permission.object.create(**row)效果一样,这里用这种方式是为了捕获唯一性错误
                try:
                    permission_obj = models.Permission(**url_form)
                    permission_obj.validate_unique()  # 检查当前对象在数据库是否存在唯一的
                    permission_obj_list.append(permission_obj)
                except Exception as e:
                    formset.errors[num].update(e)  # 把错误信息放到对应的form里面
                    generate_formset = formset  # 要把用户批量增加时出错的错误信息传给模板
                    has_repeat_error = True

            if not has_repeat_error:
                models.Permission.objects.bulk_create(permission_obj_list, batch_size=formset.total_form_count())
        else:
            generate_formset = formset  # 出错信息传给模板

    # 批量更新

    if request.method == 'POST' and post_type == 'update':
        formset = update_formset_class(data=request.POST)
        if formset.is_valid():
            url_form_list = formset.cleaned_data
            for num in range(0, formset.total_form_count()):
                url_form = url_form_list[num]
                permission_id = url_form.pop('id')
                try:
                    permission_obj = models.Permission.objects.filter(id=permission_id).first()
                    for key, value in url_form.items():
                        setattr(permission_obj, key, value)
                        permission_obj.validate_unique()
                        permission_obj.save()
                except Exception as e:
                    formset.errors[num].update(e)
                    update_formset = formset  # 要把用户批量更新时出错的错误信息传给模板
        else:
            update_formset = formset  # 出错信息传给模板

    # 1. 获取项目中所有的url

    all_url_dict = get_all_url_dict()

    router_name_set = set(all_url_dict.keys())  # 所有路由中的url集合
    """
    set里不能有重复的值，转换成set后只会剩下key
     {
     'rbac:menu_list': {'name': 'rbac:menu_list', 'url': 'xxxxx/yyyy/menu/list'}
     } 
     会变成 {'rbac:menu_list'}
    """
    #

    # 2. 获取数据库中所有的url
    all_db_permissions = models.Permission.objects.all().values('id', 'title', 'name', 'url', 'menu_id', 'pid_id')
    db_permission_name_set = set()  # 数据库中的set集合
    db_permission_dict = OrderedDict()

    for db_permission in all_db_permissions:
        db_permission_dict[db_permission[
            'name']] = db_permission  # {'rbac:menu_list':{'id':1,'title':'角色列表',name:'rbac:role_list',url:'/rbac/role/list'},}
        db_permission_name_set.add(db_permission['name'])  # {'rbac:menu_list','rbac:menu_add'......}

    for name, value in db_permission_dict.items():
        router_row_dict = all_url_dict.get(name)  # {'name':'rbac:role_list','url':'/rbac/role/list'},
        if not router_row_dict:  # 没有别名和url的直接跳过
            continue
        if value['url'] != router_row_dict['url']:  # 数据库里的url和自动发现的url进行对比
            value['url'] = '路由和数据库中的不一致'
            # 字典里的值和列表里的值用的是同一个内存地址，如果改了字典里的值，列表里相应的值也会被改。
            # 所以这个操作会修改数据库里url的值为：路由和数据库中的不一致'

    # 3. 应该添加、删除和修改的权限

    # 3.1 计算出应该添加的name
    if not generate_formset:
        """
        如果目标没有通过验证，generate_formset的值就是上面出错了的formset，就不会执行下面的代码，页面就会显示错误信息
        如果通过验证，就会返回给页面自动发现的数据库中有、路由中没有的url。
        下面的 if not update_formset同理
        """
        generate_name_list = router_name_set - db_permission_name_set
        generate_formset = generate_formset_class(
            initial=[add_url for name, add_url in all_url_dict.items() if name in generate_name_list]
        )

    # 3.2 计算出应该删除的name ： 数据库有，路由中没有
    delete_url_name_list = db_permission_name_set - router_name_set  # 数据库里的url - 路由中的url
    delete_url_list = [delete_url_obj for name, delete_url_obj in db_permission_dict.items() if
                       name in delete_url_name_list]

    # 3.3 计算出应该更新的name ：数据库和路由中都有
    if not update_formset:
        update_name_list = db_permission_name_set & router_name_set  # 都包含的元素
        update_formset = update_formset_class(
            initial=[update_url for name, update_url in db_permission_dict.items() if name in update_name_list]
        )

    context = {
        'generate_formset': generate_formset,
        'delete_url_list': delete_url_list,
        'update_formset': update_formset,
    }

    return render(request, 'rbac/multi_permissions.html', context)


def multi_permissions_delete(request, pk):
    """
    批量页面的权限删除
    :param request:
    :param pk:
    :return:
    """
    multi_pemrission_url = memory_reverse(request, 'rbac:multi_permissions')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': multi_pemrission_url})
    models.Permission.objects.filter(id=pk).delete()
    return redirect(multi_pemrission_url)


def distribute_permissions(request):
    """
    权限分配
    :param request:
    :return:
    """

    user_id = request.GET.get('uid')

    user_model_class = import_string(settings.RBAC_USER_MODEL_CLASS)
    user_object = user_model_class.objects.filter(id=user_id).first()

    if not user_object:
        user_id = None

    role_id = request.GET.get('rid')
    role_object = models.Role.objects.filter(id=role_id).first()

    if not role_object:
        role_id = None

    if request.method == 'POST' and request.POST.get('type') == 'role':
        role_id_list = request.POST.getlist('roles')
        # 用户和角色的关系添加到第三张表（关系表）
        if not user_object:
            return HttpResponse('请选择用户，然后再分配角色')
        user_object.roles.set(role_id_list)

    if request.method == 'POST' and request.POST.get('type') == 'permission':
        permission_id_list = request.POST.getlist('permissions')
        if not role_object:
            return HttpResponse('请选择角色然后再分配权限！')
        role_object.permissions.set(permission_id_list)

    # 获取当前用户拥有的所有角色

    if user_id:
        user_has_roles = user_object.roles.all()
    else:
        user_has_roles = []

    user_has_roles_dict = {item.id: None for item in user_has_roles}  # 字典查找速度更快

    # 获取当前用户拥有的所有权限
    # 如果选中了角色，优先显示选中角色所拥有的权限
    # 如果没有选角色，才显示用户所拥有的权限

    if role_object:  # 选择了角色
        user_has_permissions = role_object.permissions.all()
        user_has_permissions_dict = {item.id: None for item in user_has_permissions}
    elif user_object:  # 未选择角色，但是选择了用户
        user_has_permissions = user_object.roles.filter(permissions__id__isnull=False).values(
            'id', 'permissions').distinct()
        user_has_permissions_dict = {item['permissions']: None for item in user_has_permissions}
    else:
        user_has_permissions_dict = {}

    user_list = user_model_class.objects.all()
    all_role_list = models.Role.objects.all()

    # 用到的知识点：字典里的值和列表里的值用的是同一个内存地址，如果改了字典里的值，列表里相应的值也会被改。

    # 所有的一级菜单
    all_menu_list = models.Menu.objects.all().values('id', 'title')

    all_menu_dict = {}

    for menu_obj in all_menu_list:
        menu_obj['children'] = []  # 用于放二级菜单
        all_menu_dict[menu_obj['id']] = menu_obj

    # 所有的二级菜单
    all_second_menu_list = models.Permission.objects.filter(menu__isnull=False).values('id', 'title', 'menu_id')

    all_second_menu_dict = {}

    for second_menu_obj in all_second_menu_list:
        second_menu_obj['children'] = []  # 用于放三级菜单（具体权限）
        all_second_menu_dict[second_menu_obj['id']] = second_menu_obj
        menu_id = second_menu_obj['menu_id']
        all_menu_dict[menu_id]['children'].append(second_menu_obj)

    # 所有的三级菜单（不能做菜单的权限）
    all_permission_list = models.Permission.objects.filter(menu__isnull=True).values('id', 'title', 'pid_id')

    for permission_obj in all_permission_list:
        pid = permission_obj['pid_id']
        if not pid:  # 表示数据不合法，也就是菜单和父权限都没有，那就不处理了
            continue
        all_second_menu_dict[pid]['children'].append(permission_obj)

    """
      [
          {
              id:1,
              title:'业务管理',
              children:[
                  {
                      'id':1,
                      title:'账单列表',
                      children:[
                          {'id':12, 'title':'添加账单'}
                      ]
                  },
                  {'id':11, 'title':'客户列表'},
              ]
          },
      ]
          """

    context = {
        'user_list': user_list,
        'role_list': all_role_list,
        'all_menu_list': all_menu_list,
        'user_id': user_id,
        'user_has_roles_dict': user_has_roles_dict,
        'user_has_permissions_dict': user_has_permissions_dict,
        'role_id': role_id
    }
    return render(request, 'rbac/distribute_permissions.html', context)
