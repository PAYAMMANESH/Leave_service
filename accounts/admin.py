from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Department, OtpCode
from .forms import UserCreationForm, UserChangeForm


# Register your models here.


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ['user_id', "user_phone", "is_admin"]
    list_filter = ['is_admin']
    fieldsets = (
        (None, {"fields": ("user_id", "user_phone", "Full_name", "password", 'email')}),
        ("Permission", {"fields": (
            "is_admin", "is_active", "is_MiddleManager", "last_login", 'number_of_month_leave_left',
            'number_of_year_leave_left',
            'number_of_sick_leave_left', "number_of_with_out_pay", 'department_code')})
    )

    add_fieldsets = (
        (None, {
            "fields": {"user_id", "user_phone", "Full_name", "email", "password1", "password2", 'is_admin',
                       'is_MiddleManager',
                       'department_code'}}),
    )

    search_fields = ("user_id", "Full_name")
    ordering = ("Full_name",)
    filter_horizontal = ()


class DepartmanAdmin(admin.ModelAdmin):
    list_display = ['department_code']


# admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Department, DepartmanAdmin)
admin.site.register(OtpCode)
