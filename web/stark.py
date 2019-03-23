from stark.service.version1 import site
from web import models
from web.views.course import CourseHandler
from web.views.class_list import ClassListHandler
from web.views.consult_record import ConsultRecordHandler
from web.views.check_payment_record import CheckPaymentRecord
from web.views.department import DepartmentHandler
from web.views.public_customer import PublicCustomerHandler
from web.views.private_customer import PrivateCustomerHandler
from web.views.payment_record import PaymentRecordHandler
from web.views.school import SchoolHandler
from web.views.student import StudentHandler
from web.views.score_record import ScoreHandler
from web.views.userinfo import UserInfoHandler

site.register(models.School, SchoolHandler)
site.register(models.Department, DepartmentHandler)
site.register(models.Customer, PublicCustomerHandler, 'public')
site.register(models.Customer, PrivateCustomerHandler, 'private')
site.register(models.UserInfo, UserInfoHandler)
site.register(models.Course, CourseHandler)
site.register(models.ClassList, ClassListHandler)
site.register(models.ConsultRecord, ConsultRecordHandler)
site.register(models.PaymentRecord, PaymentRecordHandler)
site.register(models.PaymentRecord, CheckPaymentRecord, 'check')
site.register(models.Student, StudentHandler)
site.register(models.ScoreRecord, ScoreHandler)
