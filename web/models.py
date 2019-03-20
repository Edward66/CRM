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
    tutor = models.ForeignKey(verbose_name='班主任', to='UserInfo', related_name='classes', on_delete=models.CASCADE)
    tech_teacher = models.ManyToManyField(verbose_name='任课老师', to='UserInfo', related_name='teach_classes', blank=True)
    memo = models.TextField(verbose_name='说明', max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.course.title}{self.semester}期"
