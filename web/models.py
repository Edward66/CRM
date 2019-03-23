from django.db import models
from rbac.models import UserInfo as RbacUserInfo


class School(models.Model):
    """
    校区表
    """
    title = models.CharField(verbose_name='校区名称', max_length=32)

    def __str__(self):
        return self.title


class Department(models.Model):
    """
    部门表
    """
    title = models.CharField(verbose_name='部门名称', max_length=16)

    def __str__(self):
        return self.title


class UserInfo(RbacUserInfo):
    """
    员工表
    """
    MALE = 1
    FEMALE = 2
    GENDER_ITEMS = (
        (MALE, '男'),
        (FEMALE, '女'),
    )
    realname = models.CharField(verbose_name='真实姓名', max_length=16)
    phone = models.CharField(verbose_name='手机号', max_length=32)
    gender = models.PositiveIntegerField(verbose_name='性别', choices=GENDER_ITEMS, default=MALE)
    department = models.ForeignKey(to=Department, verbose_name='部门', on_delete=models.CASCADE)

    def __str__(self):
        return self.realname


class Course(models.Model):
    """
    课程表
    """
    title = models.CharField(verbose_name='课程名称', max_length=32)

    def __str__(self):
        return self.title


class ClassList(models.Model):
    """
    班级表
    """
    school = models.ForeignKey(verbose_name='校区', to='School', on_delete=models.CASCADE)
    course = models.ForeignKey(verbose_name='课程名称', to='Course', on_delete=models.CASCADE)
    semester = models.PositiveIntegerField(verbose_name='班级(期)')
    price = models.PositiveIntegerField(verbose_name='学费')
    start_date = models.DateField(verbose_name='开班日期')
    graduate_date = models.DateField(verbose_name='结课日期', null=True, blank=True)
    tutor = models.ForeignKey(verbose_name='班主任', to='UserInfo', related_name='classes',
                              limit_choices_to={'department__title': '教质部'}, on_delete=models.CASCADE)
    tech_teacher = models.ManyToManyField(verbose_name='任课老师', to='UserInfo', related_name='teach_classes', blank=True,
                                          limit_choices_to={'department__title__in': ['Python教学部', 'Linux教学部']})
    memo = models.TextField(verbose_name='说明', max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.course.title}{self.semester}期"


class Customer(models.Model):
    """
    客户表
    """
    MAX_PRIVATE_CUSTOMER_COUNT = 150

    STATUS_CHOICES = [
        (1, '已报名'),
        (2, '未报名'),
    ]

    GENDER_CHOICE = (
        (1, '男'),
        (2, '女'),
    )
    SOURCE_CHOICES = [
        (1, 'qq群'),
        (2, '内部转介绍'),
        (3, '官网推广'),
        (4, '百度推广'),
        (5, '360推广'),
        (6, '搜狗推广'),
        (7, '腾讯课堂'),
        (8, '广点通'),
        (9, '高校宣讲'),
        (10, '渠道代理'),
        (11, '51cto'),
        (12, '智汇推'),
        (13, '网盟'),
        (14, 'DSP'),
        (15, 'SEO'),
        (16, '其他'),
    ]

    EDUCATION_CHOICES = (
        (1, '重点大学'),
        (2, '普通本科'),
        (3, '独立院校'),
        (4, '民办本科'),
        (5, '大专'),
        (6, '民办大专'),
    )
    EXPERIENCE_CHOICES = [
        (1, '在校生'),
        (2, '应届毕业'),
        (3, '半年以内'),
        (4, '半年至一年'),
        (5, '一年至三年'),
        (6, '三年至五年'),
        (7, '五年以上'),
    ]
    WORK_STATUS_CHOICES = [
        (1, '在职'),
        (2, '无业'),
    ]

    name = models.CharField(verbose_name='姓名', max_length=32)
    contact_info = models.CharField(verbose_name='联系方式', max_length=64, unique=True, help_text='QQ号/微信/手机号')

    status = models.PositiveIntegerField(verbose_name='状态', choices=STATUS_CHOICES, default=2,
                                         help_text='选择客户此时的状态')
    gender = models.PositiveIntegerField(verbose_name='性别', choices=GENDER_CHOICE)
    source = models.PositiveIntegerField('客户来源', choices=SOURCE_CHOICES, default=1)
    referral_from = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        verbose_name='转介绍自学员',
        help_text='若此客户是转介绍自内部学员，请在此处选择内部学员的名字',
        related_name='internal_referral',
        on_delete=models.CASCADE,
    )
    course = models.ManyToManyField(verbose_name='课程咨询', to='Course')
    consultant = models.ForeignKey(verbose_name='课程顾问', to='UserInfo', related_name='consultant', null=True, blank=True,
                                   on_delete=models.CASCADE, limit_choices_to={'department__title': '销售部'})
    education = models.PositiveIntegerField(verbose_name='学历', choices=EDUCATION_CHOICES, blank=True, null=True)
    graduation_school = models.CharField(verbose_name='毕业学院', max_length=64, blank=True, null=True)
    major = models.CharField(verbose_name='所学专业', max_length=64, blank=True, null=True)
    experience = models.PositiveIntegerField(verbose_name='工作经验', choices=EXPERIENCE_CHOICES, blank=True, null=True)
    work_status = models.PositiveIntegerField(verbose_name='职业状态', choices=WORK_STATUS_CHOICES, default=1, blank=True,
                                              null=True)
    company = models.CharField(verbose_name='目前就职公司', max_length=64, blank=True, null=True)
    salary = models.CharField(verbose_name='当前薪资', max_length=64, blank=True, null=True)
    date = models.DateField(verbose_name='咨询日期', auto_now_add=True)
    last_consult_date = models.DateField(verbose_name='最后跟进日期', auto_now_add=True)

    def __str__(self):
        return f'姓名：{self.name},联系方式：{self.contact_info}'


class ConsultRecord(models.Model):
    """
    客户跟进记录
    """
    customer = models.ForeignKey(verbose_name='所咨询客户', to='Customer', on_delete=models.CASCADE)
    consultant = models.ForeignKey(verbose_name='跟踪人', to='UserInfo', on_delete=models.CASCADE)
    note = models.TextField(verbose_name='跟进内容')
    date = models.DateField(verbose_name='跟进日期', auto_now_add=True)


class PaymentRecord(models.Model):
    """
    缴费申请
    """
    PAY_TYPE_CHOICES = [
        (1, '报名费'),
        (2, '学费'),
        (3, '退学'),
        (4, '其他'),
    ]
    CONFIRM_STATUS_CHOICES = [
        (1, '申请中'),
        (2, '已确认'),
        (3, '已驳回'),
    ]
    customer = models.ForeignKey(verbose_name='客户', to='Customer', on_delete=models.CASCADE)
    consultant = models.ForeignKey(verbose_name='课程顾问', to='UserInfo', help_text='谁签的单选谁', on_delete=models.CASCADE)
    pay_type = models.IntegerField(verbose_name='费用类型', choices=PAY_TYPE_CHOICES, default=1)
    paid_fee = models.IntegerField(verbose_name='金额', default=0)
    class_list = models.ForeignKey(verbose_name='申请班级', to='ClassList', on_delete=models.CASCADE)
    apply_date = models.DateTimeField(verbose_name='申请日期', auto_now_add=True)
    confirm_status = models.PositiveIntegerField(verbose_name='确认状态', choices=CONFIRM_STATUS_CHOICES, default=1)
    confirm_date = models.DateTimeField(verbose_name='确认日期', null=True, blank=True)
    confirm_user = models.ForeignKey(verbose_name='审批人', to='UserInfo', related_name='confirms', null=True, blank=True,
                                     on_delete=models.CASCADE)
    note = models.TextField(verbose_name='备注', blank=True, null=True)


class Student(models.Model):
    """
    学生表
    """
    STUDENT_STATUS_CHOICES = [
        (1, '申请中'),
        (2, '在读'),
        (3, '毕业'),
        (4, '退学')
    ]
    customer = models.OneToOneField(verbose_name='客户信息', to='Customer', on_delete=models.CASCADE)
    qq = models.CharField(verbose_name='QQ号', max_length=32)
    mobile = models.CharField(verbose_name='手机号', max_length=32)
    emergency_contact = models.CharField(verbose_name='紧急联系人电话', max_length=32)
    class_list = models.ManyToManyField(verbose_name='已报班级', to='ClassList', blank=True)  # m2m默认可以为空，不用设置null
    student_status = models.PositiveIntegerField(verbose_name='学员状态', choices=STUDENT_STATUS_CHOICES, default=1)
    memo = models.CharField(verbose_name='备注', max_length=255, blank=True, null=True)

    def __str__(self):
        return self.customer.name
