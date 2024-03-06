from django.db import models
from accounts.models import User


# Create your models here.

class Leave_Request(models.Model):
    LEAVE_TYPES = (
        ('entitlement', 'استحقاقی'),
        ('illness', 'استعلاجی'),
        ('unpaid', 'بدون حقوق')
    )
    STATE_TYPES = (
        ('accept', 'پذیرفته شده'),
        ('decline', 'رد شده'),
        ('pending', 'در حال بررسی'),
    )
    LEAVE_TYPE_TYPE = (
        ('hourly', 'ساعتی'),
        ('daily', 'روزانه'),
    )
    state = models.CharField(max_length=50, choices=STATE_TYPES, default='pending')
    Reason = models.TextField()
    from_hour = models.TimeField(null=True, blank=True)
    to_hour = models.TimeField(null=True, blank=True)
    work_day = models.IntegerField(null=True, blank=True)
    from_day = models.DateField(null=True, blank=True)
    to_day = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_leave')
    Leave_type = models.CharField(max_length=50, choices=LEAVE_TYPES)
    Leave_type_type = models.CharField(max_length=50, choices=LEAVE_TYPE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    admin_reason = models.TextField(blank=True, null=True)
