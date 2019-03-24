from django.conf import settings


class PermissionHanlder(object):
    #  是否显示添加按钮
    def get_add_btn(self, request, *args, **kwargs):
        # 当前用户所有的权限信息
        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
        if self.get_add_url_name not in permission_dict:
            return None
        else:
            return super().get_add_btn(request, *args, **kwargs)

    # 是否显示编辑和删除按钮（后期如果对别的权限粒度进行控制，可以在这里扩展）
    def get_list_display(self, request, *args, **kwargs):
        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
        values = []
        if self.list_display:
            values.extend(self.list_display)
            if self.get_edit_url_name in permission_dict and self.get_delete_url_name in permission_dict:
                values.append(type(self).display_edit_del)
                return values
            if self.get_edit_url_name in permission_dict:
                values.append(type(self).display_edit)
                return values

            if self.get_delete_url_name in permission_dict:
                values.append(type(self).display_del)
                return values
        return values
