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
        return self.name


class Course(models.Model):
    """
    课程表
    """
    title = models.CharField(verbose_name='课程名称', max_length=32)

    def __str__(self):
        return self.title
