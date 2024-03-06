from django.shortcuts import render, redirect
from django.views import View
from .forms import UserLogin, UserRegisterForm, UserChangePassword, AddDepartmentForm, VerifyCodeForm, enter_phone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout, authenticate
from .models import User, Department, OtpCode
from jdatetime import date as jdate
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from utils import send_otp_code
import random


# Create your views here.

class HomePage(View):
    def get(self, request):
        return render(request, 'accounts/homepage.html')


class homepage(LoginRequiredMixin, View):

    def get(self, request):
        user = User.objects.get(user_id=request.user.user_id)
        if user.is_phone_number:
            current_date = jdate.today()
            if current_date.day == 1 and current_date.month == 1:
                user.number_of_year_leave_left = 208
                user.number_of_sick_leave_left = 24
            elif current_date.day == 1:
                user.number_of_month_leave_left = 20
            month_day = user.number_of_month_leave_left // 60 // 8
            month_hour = user.number_of_month_leave_left // 60 % 8
            month_min = user.number_of_month_leave_left % 60
            sick_day = user.number_of_sick_leave_left // 60 // 8
            sick_hour = user.number_of_sick_leave_left // 60 % 8
            sick_min = user.number_of_sick_leave_left % 60
            year_day = user.number_of_year_leave_left // 60 // 8
            year_hour = user.number_of_year_leave_left // 60 % 8
            year_min = user.number_of_year_leave_left % 60
            month_left = 1200 - user.number_of_month_leave_left
            month_day_get = month_left // 60 // 8
            month_hour_get = month_left // 60 % 8
            month_min_get = month_left % 60
            year_left = 13440 - user.number_of_year_leave_left
            year_day_get = year_left // 60 // 8
            year_hour_get = year_left // 60 % 8
            year_min_get = year_left = month_left % 60
            sick_left = 1440 - user.number_of_sick_leave_left
            sick_day_get = sick_left // 60 // 8
            sick_hour_get = sick_left // 60 % 8
            sick_min_get = sick_left % 60
            return render(request, 'accounts/home.html',
                          context={'user': user, 'month_day': month_day, 'month_hour': month_hour,
                                   'month_min': month_min, 'sick_day': sick_day,
                                   'sick_hour': sick_hour, 'sick_min': sick_min, 'year_day': year_day,
                                   'year_hour': year_hour, 'year_min': year_min,
                                   'month_left': month_left, 'year_left': year_left, 'sick_left': sick_left,
                                   'month_day_get': month_day_get, 'month_hour_get': month_hour_get,
                                   "month_min_get": month_min_get,
                                   "year_day_get": year_day_get, "year_hour_get": year_hour_get,
                                   "year_min_get": year_min_get,
                                   "sick_day_get": sick_day_get, "sick_hour_get": sick_hour_get,
                                   "sick_min_get": sick_min_get})
        else:
            random_code = random.randint(1000, 9999)
            send_otp_code(phone_number=user.user_phone, code=random_code)
            OtpCode.objects.create(phone_number=user.user_phone, code=random_code)
            messages.success(request, "کد احراز هویت برای شماره تماس شما ارسال گردید", "success")
            return redirect("accounts:verify_phone")


class UserVerifyPhone(LoginRequiredMixin, View):
    form_class = VerifyCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, "accounts/verify.html", context={"form": form})

    def post(self, request):
        user_phone = request.user.user_phone
        code = OtpCode.objects.get(phone_number=user_phone)
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if code.code == cd["code"]:
                user = User.objects.get(user_id=request.user.user_id)
                user.is_phone_number = True
                user.save()
                messages.success(request, "شماره تماس شما با موفقیت اعتبار سنجی شد", "success")
                code.delete()
                return redirect("accounts:userhome")
            return redirect("accounts:verify_code")
        return redirect("accounts:userhome")


class ChangeProf(LoginRequiredMixin, View):

    def get(self, request, userid):
        return render(request, 'accounts/changeprof.html')

    def post(self, request, userid):
        user = User.objects.get(user_id=userid)
        user.Full_name = request.POST.get('Full_name')
        # user.user_id = request.POST.get('user_id')
        user.user_phone = request.POST.get('user_phone')
        user.email = request.POST.get('email')
        user.is_phone_number = False
        user.save()
        return redirect('accounts:userhome')


class UserLogin(View):
    form_class = UserLogin

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/login.html', context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, user_id=cd['user_id'], password=cd['password'])
            if user is not None:
                LogginUser = User.objects.get(user_id=cd['user_id'])
                if LogginUser.is_admin:
                    login(request, user)
                    messages.success(request, "مدیر ارشد شما با موفقیت وارد شدید", 'success')
                    return redirect('accounts:userhome')
                elif LogginUser.is_MiddleManager:
                    login(request, user)
                    messages.success(request, 'مدیر میانی شما با موفقیت وارد شدید', 'success')
                    return redirect('accounts:userhome')
                else:
                    login(request, user)
                    messages.success(request, 'با موفقیت وارد شدید', 'success')
                    return redirect('accounts:userhome')
            messages.error(request, 'نام کاربری یا رمز عبور صحیح نمی باشد', 'warning')
            return redirect('accounts:userlogin')
        messages.error(request, 'نام کاربری یا رمز عبور صحیح نمی باشد', 'danger')
        return redirect('accounts:userlogin')


class UserLogout(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'کاربر گرامی شما با موفقیت ازحساب کاربری خود خارج شدید', 'success')
        return redirect('accounts:userlogin')


class UserRegister(LoginRequiredMixin, View):
    form_class = UserRegisterForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_admin or request.user.is_MiddleManager:
            return super().dispatch(request, *args, **kwargs)
        else:
            return render(request, 'accounts/user_page.html')

    def get(self, request, dp_code):
        form = self.form_class
        return render(request, 'accounts/register.html', context={'form': form})

    def post(self, request, dp_code):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.filter(user_id=cd['user_id']).exists()
            if not user:
                NewUser = User.objects.create_user(user_phone=cd['user_phone'],
                                                   user_id=cd['user_id'],
                                                   Full_name=cd['Full_name'],
                                                   password=cd['password'],
                                                   email=cd['email'])
                # NewUser.department_code = Department.objects.get(department_code=dp_code)
                NewUser.department_code.set(dp_code)
                NewUser.save()
                return redirect('accounts:departman_detail', dp_code)
            else:
                messages.error(request, 'با این کد کاربری قبلا کاربری افزوده شده است', 'warning')
                return redirect('accounts:userregister', dp_code)
        return render(request, 'accounts/register.html', context={'form': form})


class ManagerRegister(LoginRequiredMixin, View):
    form_class = UserRegisterForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_admin:
            return super().dispatch(request, *args, **kwargs)
        else:
            return render(request, 'accounts/user_page.html')

    def get(self, request, dp_code):
        form = self.form_class
        return render(request, 'accounts/register.html', context={'form': form})

    def post(self, request, dp_code):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            NewUser = User.objects.create_user(user_phone=cd['user_phone'],
                                               user_id=cd['user_id'],
                                               Full_name=cd['Full_name'],
                                               password=cd['password'],
                                               email=cd['email'])
            NewUser.department_code.add(Department.objects.get(department_code=dp_code))
            NewUser.is_MiddleManager = True
            NewUser.save()
            return redirect('accounts:departman_detail', dp_code)
        return render(request, 'accounts/register.html', context={'form': form})


class UserChangePass(LoginRequiredMixin, View):
    form_class = UserChangePassword

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/changepass.html', context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.get(user_id=request.user.user_id)
            user.set_password(cd['password'])
            user.save()
            messages.success(request, 'گذرواژه شما با موفقیت تغییر یافت', 'success')
            return redirect('accounts:userlogin')
        return render(request, 'accounts/changepass.html', context={'form': form})


class DepartmanView(LoginRequiredMixin, View):
    def get(self, request):
        all_departman = Department.objects.all()
        if request.user.is_admin:
            return render(request, 'accounts/departman.html', context={'departman': all_departman})
        else:
            user = User.objects.get(user_id=request.user.user_id)
            user_departments = Department.objects.filter(user_department__user_id=user.user_id)
            return render(request, 'accounts/departman.html', context={'departman': user_departments})


class AddDepartmanView(LoginRequiredMixin, View):
    form_class = AddDepartmentForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_admin:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('accounts:departman')

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/add_department.html', context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            departman = Department.objects.filter(department_name=cd['department_name']).exists()
            if not departman:
                departman = Department.objects.create(
                    department_name=cd['department_name'])
                departman.save()
                messages.success(request, 'دپارتمان با موفقیت افزوده شد', 'success')
                return redirect('accounts:departman')
            else:
                messages.error(request, '.با این نام قبلا دپارتمان ثبت شده است', 'warning')
                return render(request, 'accounts/add_department.html', context={'form': form})
        else:
            messages.warning(request, 'اطلاعات به درستی وارد نشده اند', 'error')
            return render(request, 'accounts/add_department.html', context={'form': form})


class DepartamnDelete(LoginRequiredMixin, View):
    def get(self, request, dp_code):
        if request.user.is_admin:
            departman = Department.objects.get(department_code=dp_code)
            departman.delete()
            messages.success(request, 'دپارتمان مورد نظر با موفقیت حذف گردید', 'success')
            return redirect('accounts:departman')
        else:
            messages.error(request, 'شما امکان حذف دپارتمان را ندارید', 'warning')
            return redirect('accounts:departman')


class DepartmanDetailview(LoginRequiredMixin, View):
    def get(self, request, dp_code):
        departman = Department.objects.get(department_code=dp_code)
        user = departman.user_department.all()
        manager = departman.user_department.filter(is_MiddleManager=True)
        return render(request, 'accounts/departman_detail.html',
                      context={'departman': departman, 'user': user, 'manager': manager})


class ShowEmployee(LoginRequiredMixin, View):
    def get(self, request, dp_code):
        user = User.objects.filter(department_code=None, is_admin=False, is_MiddleManager=False)
        return render(request, 'accounts/show_employee.html', context={'user': user, 'dp_code': dp_code})


class AddOldEmployee(LoginRequiredMixin, View):
    def get(self, request, userid, dp_code):
        user = User.objects.get(user_id=userid)
        dp = Department.objects.get(department_code=dp_code)
        user.department_code.add(dp)
        user.save()
        messages.success(request, 'کاربر با موفقیت افزوده شد', 'success')
        return redirect('accounts:departman_detail', dp_code)


class ShowDepartmentEmployee(LoginRequiredMixin, View):
    def get(self, request, dp_code):
        dp = Department.objects.get(department_code=dp_code)
        if request.user.is_admin:
            user = User.objects.filter(department_code=dp, is_admin=False)
            return render(request, 'accounts/delete_employee.html', context={'user': user, 'dp_code': dp_code})
        elif request.user.is_MiddleManager:
            user = User.objects.filter(department_code=dp, is_MiddleManager=False, is_admin=False)
            return render(request, 'accounts/delete_employee.html', context={'user': user, 'dp_code': dp_code})


class DeleteEmployee(LoginRequiredMixin, View):
    def get(self, request, user_id, dp_code):
        user = User.objects.get(user_id=user_id)
        user.department_code.remove(dp_code)
        user.save()
        messages.success(request, 'کاربر با موفقیت حذف شد', 'success')
        return redirect('accounts:departman_detail', dp_code)


class ShowManager(LoginRequiredMixin, View):
    def setup(self, request, *args, **kwargs):
        if request.user.is_admin:
            return super().setup(request, *args, **kwargs)
        else:
            return redirect('accounts:departman_detail', kwargs['dp_code'])

    def get(self, request, dp_code):
        user = User.objects.filter(is_MiddleManager=True)
        return render(request, 'accounts/show_manager.html', context={'user': user, 'dp_code': dp_code})


class AddOldManager(LoginRequiredMixin, View):
    def setup(self, request, *args, **kwargs):
        if request.user.is_admin:
            return super().setup(request, *args, **kwargs)
        else:
            return redirect('accounts:departman_detail', kwargs['dp_code'])

    def get(self, request, user_id, dp_code):
        dp = Department.objects.get(department_code=dp_code)
        user = User.objects.get(user_id=user_id)
        user.department_code = dp
        messages.success(request, 'مدیر با موفقیت انتخاب شد', 'success')
        return redirect('accounts:departman_detail', dp_code)


class ForgotPassword(View):
    form_class = enter_phone

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/enter_phone.html', context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if User.objects.filter(user_phone=cd['phone']).exists():
                random_code = random.randint(1000, 9999)
                send_otp_code(phone_number=cd['phone'], code=random_code)
                OtpCode.objects.create(phone_number=cd['phone'], code=random_code)
                user = User.objects.get(user_phone=cd['phone'])
                request.session["user_info"] = {
                    "phone_number": cd['phone'],
                    "email": user.email,
                    "full_name": user.Full_name,
                }
                messages.success(request, "کد احراز هویت برای شماره تماس شما ارسال گردید", "success")
                return redirect("accounts:verify_forgot_pass_code", cd['phone'])
            else:
                messages.error(request, "کاربر یافت نشد", "warning")
                return redirect("accounts:verify_forgot_pass_code", cd['phone'])

        return redirect('accounts:forgot_pass')


class VerifyForgotPassCode(View):
    form_class = VerifyCodeForm

    def get(self, request, phone):
        form = self.form_class
        return render(request, "accounts/verify.html", context={"form": form})

    def post(self, request, phone):
        code = OtpCode.objects.get(phone_number=phone)
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if code.code == cd["code"]:
                user = User.objects.get(user_phone=phone)
                code.delete()
                return redirect("accounts:password_reset_complete", user.user_id)
            return redirect("accounts:verify_forgot_pass_code")
        return redirect("accounts:verify_forgot_pass_code")


class UserforgotPass(View):
    form_class = UserChangePassword

    def get(self, request, userid):
        form = self.form_class
        return render(request, 'accounts/changepass.html', context={'form': form})

    def post(self, request, userid):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.get(user_id=userid)
            user.set_password(cd['password'])
            user.save()
            messages.success(request, 'گذرواژه با موفقیت تغییر یافت', 'success')
            return redirect('accounts:userlogin')
        return render(request, 'accounts/changepass.html', context={'form': form})
