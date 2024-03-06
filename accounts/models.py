from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import UserManager


# Create your models here.
class Department(models.Model):
    department_code = models.AutoField(primary_key=True, unique=True)
    department_name = models.CharField(max_length=50, unique=True)


class User(AbstractBaseUser):
    user_id = models.CharField(max_length=10, primary_key=True, unique=True)
    user_phone = models.CharField(max_length=11, unique=True)
    Full_name = models.CharField(max_length=50)
    #number_of_month_leave_left = models.IntegerField(default=20)
    number_of_month_leave_left = models.IntegerField(default=1200)
    #number_of_year_leave_left = models.IntegerField(default=208)
    number_of_year_leave_left = models.IntegerField(default=13440)
    #number_of_sick_leave_left = models.IntegerField(default=24)
    number_of_sick_leave_left = models.IntegerField(default=1440)
    department_code = models.ManyToManyField(Department,
                                             related_name='user_department')
    email = models.EmailField(unique=True)
    number_of_with_out_pay = models.IntegerField(default=0)
    is_MiddleManager = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_phone_number = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['user_phone', "Full_name", "email"]

    def __str__(self):
        return self.user_id

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_lable):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.phone_number} - {self.code} - {self.created}"