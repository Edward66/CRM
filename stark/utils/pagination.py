"""
分页组件
"""


class Pagination(object):
    def __init__(self, current_page, all_count, base_url, query_params, per_page_data, display_page_number=11):
        """
        分页初始化
        :param current_page: 当前页码
        :param all_count: 数据库中总条数
        :param base_url: 基础URL
        :param query_params: Querydict对象，内部含所有当前URL的原条件
        :param per_page_data: 每页显示数据条数
        :param display_page_number: 页面上最多显示的页码数量
        """
        self.base_url = base_url
        try:
            self.current_page = int(current_page)
            if self.current_page <= 0:
                raise Exception()
        except Exception as e:
            self.current_page = 1
        self.all_count = all_count
        self.query_params = query_params
        self.per_page_data = per_page_data
        self.display_page_number = display_page_number
        real_page_number, remainder = divmod(self.all_count, self.per_page_data)
        if remainder != 0:
            real_page_number += 1
        self.real_page_number = real_page_number

        half_page_number = int(self.display_page_number / 2)
        self.half_page_number = half_page_number

    @property
    def start(self):
        """
        数据获取值起始索引
        :param self:
        :return:
        """
        return (self.current_page - 1) * self.per_page_data

    @property
    def end(self):
        """
        数据获取值结束索引
        :return:
        """
        return self.current_page * self.per_page_data

    def page_html(self):
        """
        生成HTML页码
        :return:
        """
        # 如果数据总页码real_page_number < 11 --> display_page_number
        if self.real_page_number < self.display_page_number:
            pager_start = 1
            pager_end = self.real_page_number

        else:
            # 数据页码已经超过11
            # 判断：如果当前页 <=5 -->   half_page_number
            if self.current_page <= self.half_page_number:
                pager_start = 1
                pager_end = self.display_page_number
            else:
                # 如果：当前页+5 > 总页码
                if (self.current_page + self.half_page_number) > self.real_page_number:
                    pager_start = self.real_page_number - self.display_page_number + 1
                    pager_end = self.real_page_number
                else:
                    pager_start = self.current_page - self.half_page_number
                    pager_end = self.current_page + self.half_page_number

        page_list = []

        if self.current_page <= 1:
            prev = '<li><a href="#">上一页</a></li>'
        else:
            self.query_params['page'] = self.current_page - 1
            # urlencode：Return an encoded string of all query string arguments.
            prev = '<li><a href="%s?%s">上一页</a></li>' % (self.base_url, self.query_params.urlencode())
        page_list.append(prev)

        for i in range(pager_start, pager_end + 1):
            self.query_params['page'] = i
            if self.current_page == i:
                tpl = '<li class="active"><a href="%s?%s">%s</a></li>' % (
                    self.base_url, self.query_params.urlencode(), i,)
            else:
                tpl = '<li><a href="%s?%s">%s</a></li>' % (self.base_url, self.query_params.urlencode(), i,)
            page_list.append(tpl)

        if self.current_page >= self.real_page_number:
            nex = '<li><a href="#">下一页</a></li>'
        else:
            self.query_params['page'] = self.current_page + 1
            nex = '<li><a href="%s?%s">下一页</a></li>' % (self.base_url, self.query_params.urlencode(),)
        page_list.append(nex)
        page_str = "".join(page_list)
        return page_str
