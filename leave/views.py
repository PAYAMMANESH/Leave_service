from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AddUserLeaveRequestForm, AdminReason
from accounts.models import User
from .models import Leave_Request
from django.contrib import messages
from datetime import datetime
from accounts.models import Department


# Create your views here.


class UserRequest(LoginRequiredMixin, View):

    def get(self, request):
        userrequest = Leave_Request.objects.filter(user=User.objects.get(user_id=request.user.user_id))
        return render(request, 'leave/request.html', context={'userrequest': userrequest})


class AcceptUserRequest(LoginRequiredMixin, View):

    def get(self, request, leave_id):
        leave = Leave_Request.objects.get(id=leave_id)
        leave.save()
        if leave.Leave_type == 'illness':
            if leave.Leave_type_type == 'hourly':
                from_datetime = datetime.combine(datetime.today(), leave.from_hour)
                to_datetime = datetime.combine(datetime.today(), leave.to_hour)
                time_difference = to_datetime - from_datetime
                #total_minutes = (time_difference.seconds) // 60
                total_minutes = (time_difference.seconds) / 60
                #if leave.user.number_of_sick_leave_left * 60 >= total_minutes:
                if leave.user.number_of_sick_leave_left >= total_minutes:
                    leave.state = 'accept'
                    leave.save()
                    if total_minutes > 360:
                        total_minutes = 480
                    #leave.user.number_of_sick_leave_left = (leave.user.number_of_sick_leave_left * 60 - total_minutes) // 60
                    leave.user.number_of_sick_leave_left = (leave.user.number_of_sick_leave_left - total_minutes)
                    leave.user.save()
                    messages.success(request, 'درخواست با موفقیت تایید شد', 'success')
                    return redirect('leave:checkrequest')
                else:
                    messages.error(request, 'با درخواست شما موافقت نشد', 'warning')
                    leave.state = 'decline'
                    leave.save()
                    return redirect('leave:checkrequest')
            else:
                number_of_work_day = leave.work_day
                total_minutes = number_of_work_day * 8 * 60
                #if leave.user.number_of_sick_leave_left * 60 >= total_minutes:
                if leave.user.number_of_sick_leave_left >= total_minutes:
                    leave.state = 'accept'
                    leave.save()
                    #leave.user.number_of_sick_leave_left = (leave.user.number_of_sick_leave_left * 60 - total_minutes) // 60
                    leave.user.number_of_sick_leave_left = (leave.user.number_of_sick_leave_left - total_minutes)
                    leave.user.save()
                    messages.success(request, 'درخواست با موفقیت تایید شد', 'success')
                    return redirect('leave:checkrequest')
                else:
                    messages.error(request, 'با درخواست شما موافقت نشد', 'warning')
                    leave.state = 'decline'
                    leave.save()
                    return redirect('leave:checkrequest')
        elif leave.Leave_type == 'entitlement':
            if leave.Leave_type_type == 'hourly':
                from_datetime = datetime.combine(datetime.today(), leave.from_hour)
                to_datetime = datetime.combine(datetime.today(), leave.to_hour)
                time_difference = to_datetime - from_datetime
                #total_minutes = (time_difference.seconds) // 60
                total_minutes = (time_difference.seconds) / 60
                #if leave.user.number_of_month_leave_left * 60 >= total_minutes:
                if total_minutes > 360:
                    total_minutes = 480
                if leave.user.number_of_month_leave_left >= total_minutes:
                    leave.state = 'accept'
                    leave.save()
                    #leave.user.number_of_month_leave_left = (leave.user.number_of_month_leave_left * 60 - total_minutes) // 60
                    leave.user.number_of_month_leave_left = (leave.user.number_of_month_leave_left - total_minutes)
                    #leave.user.number_of_year_leave_left = (leave.user.number_of_year_leave_left * 60 - total_minutes) // 60
                    leave.user.number_of_year_leave_left = (leave.user.number_of_year_leave_left - total_minutes)
                    leave.user.save()
                    messages.success(request, 'درخواست با موفقیت تایید شد', 'success')
                    return redirect('leave:checkrequest')
                #elif leave.user.number_of_year_leave_left * 60 >= total_minutes:
                elif leave.user.number_of_year_leave_left >= total_minutes:
                    leave.state = 'accept'
                    leave.save()
                    new_total = total_minutes - leave.user.number_of_month_leave_left
                    leave.user.number_of_month_leave_left = 0

                    #leave.user.number_of_year_leave_left = (leave.user.number_of_year_leave_left * 60 - total_minutes) // 60
                    leave.user.number_of_year_leave_left = (leave.user.number_of_year_leave_left - new_total)
                    leave.user.save()
                    messages.success(request, 'درخواست با موفقیت تایید شد', 'success')
                    return redirect('leave:checkrequest')
                else:
                    messages.error(request, 'با درخواست شما موافقت نشد', 'warning')
                    leave.state = 'decline'
                    leave.save()
                    return redirect('leave:checkrequest')
            else:
                number_of_work_day = leave.work_day
                total_minutes = number_of_work_day * 8 * 60
                #if leave.user.number_of_month_leave_left * 60 >= total_minutes:
                if leave.user.number_of_month_leave_left >= total_minutes:
                    leave.state = 'accept'
                    leave.save()
                    #leave.user.number_of_month_leave_left = (leave.user.number_of_month_leave_left * 60 - total_minutes) // 60
                    leave.user.number_of_month_leave_left = (leave.user.number_of_month_leave_left - total_minutes)
                    #leave.user.number_of_year_leave_left = (leave.user.number_of_year_leave_left * 60 - total_minutes) // 60
                    leave.user.number_of_year_leave_left = (leave.user.number_of_year_leave_left - total_minutes)
                    leave.user.save()
                    messages.success(request, 'درخواست با موفقیت تایید شد', 'success')
                    return redirect('leave:checkrequest')
                #elif leave.user.number_of_year_leave_left * 60 >= total_minutes:
                elif leave.user.number_of_year_leave_left >= total_minutes:
                    leave.state = 'accept'
                    leave.save()
                    new_total = total_minutes - leave.user.number_of_month_leave_left
                    leave.user.number_of_month_leave_left = 0

                    #leave.user.number_of_year_leave_left = (leave.user.number_of_year_leave_left * 60 - total_minutes) // 60
                    leave.user.number_of_year_leave_left = (leave.user.number_of_year_leave_left - new_total)
                    leave.user.save()
                    messages.success(request, 'درخواست با موفقیت تایید شد', 'success')
                    return redirect('leave:checkrequest')
                else:
                    messages.error(request, 'با درخواست شما موافقت نشد', 'warning')
                    leave.state = 'decline'
                    leave.save()
                    return redirect('leave:checkrequest')
        else:
            leave.state = 'accept'
            leave.save()
            user = User.objects.get(user_id=leave.user.user_id)
            if leave.Leave_type_type == 'hourly':
                from_datetime = datetime.combine(datetime.today(), leave.from_hour)
                to_datetime = datetime.combine(datetime.today(), leave.to_hour)
                time_difference = to_datetime - from_datetime
                #total_minutes = (time_difference.seconds) // 60
                total_minutes = (time_difference.seconds) / 60
                #user.number_of_with_out_pay = (user.number_of_with_out_pay * 60 + total_minutes) // 60
                user.number_of_with_out_pay = (user.number_of_with_out_pay + total_minutes)
                user.save()
            else:
                number_of_work_day = leave.work_day
                total_minutes = number_of_work_day * 8 * 60
                #user.number_of_with_out_pay = (user.number_of_with_out_pay * 60 + total_minutes) // 60
                user.number_of_with_out_pay = (user.number_of_with_out_pay + total_minutes)
                user.save()
            messages.success(request, 'درخواست با موفقیت تایید شد', 'success')
            return redirect('leave:checkrequest')


class AddUserLeaveRequest(LoginRequiredMixin, View):
    form_class = AddUserLeaveRequestForm

    def get(self, request):
        form = self.form_class
        return render(request, 'leave/AddRequest.html', context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['Leave_type_type'] == 'daily':
                if ((int(cd['to_day'].day) >= int(cd['from_day'].day)) or (
                        int(cd['to_day'].month) > int(cd['from_day'].month))):
                    new_form = form.save(commit=False)
                    new_form.user = User.objects.get(user_id=request.user.user_id)
                    new_form.save()
                    if request.user.is_admin:
                        leave = Leave_Request.objects.filter(
                            user__user_id=User.objects.get(user_id=request.user.user_id)).latest('id')
                        accept_request_view = AcceptUserRequest()
                        accept_request_view.get(request, leave.id)
                    messages.success(request, "درخواست شما با موفقیت افزوده شد", 'success')
                    return redirect("leave:userequest")
                else:
                    messages.error(request, "تداخل روز شروع با روز پایان", 'warning')
                    return render(request, 'leave/AddRequest.html', context={"form": form})
            else:
                from_datetime = datetime.combine(datetime.today(), cd['from_hour'])
                to_datetime = datetime.combine(datetime.today(), cd['to_hour'])
                time_difference = to_datetime - from_datetime
                if not time_difference.days:
                    new_form = form.save(commit=False)
                    new_form.user = User.objects.get(user_id=request.user.user_id)
                    new_form.save()
                    if request.user.is_admin:
                        leave = Leave_Request.objects.filter(
                            user__user_id=User.objects.get(user_id=request.user.user_id)).latest('id')
                        accept_request_view = AcceptUserRequest()
                        accept_request_view.get(request, leave.id)
                    messages.success(request, "درخواست با موفقیت افزوده شد", 'success')
                    return redirect("leave:userequest")
                else:
                    messages.error(request, "تداخل ساعت شروع با ساعت پایان", 'warning')
                    return render(request, 'leave/AddRequest.html', context={"form": form})
        else:
            return render(request, 'leave/AddRequest.html', context={"form": form})


class AddAndAcceptLeave(LoginRequiredMixin, View):
    form_class = AddUserLeaveRequestForm

    def get(self, request, user_id):
        form = self.form_class
        return render(request, 'leave/AddRequest.html', context={'form': form})

    def post(self, request, user_id):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['Leave_type_type'] == 'daily':
                if ((int(cd['to_day'].day) >= int(cd['from_day'].day)) or (
                        int(cd['to_day'].month) > int(cd['from_day'].month))):
                    new_form = form.save(commit=False)
                    new_form.user = User.objects.get(user_id=request.user.user_id)
                    new_form.save()
                    if request.user.is_admin:
                        leave = Leave_Request.objects.filter(
                            user__user_id=User.objects.get(user_id=request.user.user_id)).latest('id')
                        accept_request_view = AcceptUserRequest()
                        accept_request_view.get(request, leave.id)
                    messages.success(request, "درخواست با موفقیت افزوده شد", 'success')
                    return redirect("leave:userequest")
                else:
                    messages.error(request, "تداخل روز شروع با روز پایان", 'warning')
                    return render(request, 'leave/AddRequest.html', context={"form": form})
            else:
                from_datetime = datetime.combine(datetime.today(), cd['from_hour'])
                to_datetime = datetime.combine(datetime.today(), cd['to_hour'])
                time_difference = to_datetime - from_datetime
                if not time_difference.days:
                    new_form = form.save(commit=False)
                    new_form.user = User.objects.get(user_id=request.user.user_id)
                    new_form.save()
                    if request.user.is_admin:
                        leave = Leave_Request.objects.filter(
                            user__user_id=User.objects.get(user_id=request.user.user_id)).latest('id')
                        accept_request_view = AcceptUserRequest()
                        accept_request_view.get(request, leave.id)
                    messages.success(request, "درخواست با موفقیت افزوده شد", 'success')
                    return redirect("leave:userequest")
                else:
                    messages.error(request, "تداخل ساعت شروع با ساعت پایان", 'warning')
                    return render(request, 'leave/AddRequest.html', context={"form": form})
        else:
            return render(request, 'leave/AddRequest.html', context={"form": form})


class AddEmployeeLeaveRequest(LoginRequiredMixin, View):
    def setup(self, request, *args, **kwargs):
        if request.user.is_admin or request.user.is_MiddleManager:
            return super().setup(request, *args, **kwargs)
        else:
            return redirect('leave:userequest')

    def get(self, request):

        if request.user.is_admin:
            user = User.objects.filter(is_MiddleManager=True)
            return render(request, 'leave/add_employee_request.html', {'form': user})
        elif request.user.is_MiddleManager:
            dp_code = User.objects.get(user_id=request.user.user_id).department_code.department_code
            departman = Department.objects.get(department_code=dp_code)
            user = User.objects.filter(is_admin=False, is_MiddleManager=False, department_code=departman)
            return render(request, 'leave/add_employee_request.html', {'form': user})


class UserRequestDetail(LoginRequiredMixin, View):
    form_class = AddUserLeaveRequestForm
    form_class2 = AdminReason

    def get(self, request, re_id):
        leave = Leave_Request.objects.get(id=re_id)
        form = self.form_class(instance=leave)
        form2 = self.form_class2(instance=leave)

        return render(request, 'leave/update_request.html', context={"form": form, 'id': re_id, 'form2': form2})

    def post(self, request, re_id):
        leave = Leave_Request.objects.get(id=re_id)
        form = self.form_class(request.POST, instance=leave)
        if leave.state == 'pending':
            if form.is_valid():
                form.save()
                messages.success(request, 'درخواست با موفقیت بروزرسانی شد')
                return redirect('leave:userequest')
            return render(request, 'leave/update_request.html', context={"form": form, 'id': re_id})
        else:
            messages.error(request, 'شما امکان بروزرسانی این درخواست را ندارید', 'warning')
            return redirect('leave:userequest')


class UserRequestDelete(LoginRequiredMixin, View):
    def get(self, request, re_id):
        leave = Leave_Request.objects.get(id=re_id)
        if leave.state == 'pending':
            leave.delete()
            messages.success(request, 'درخواست با موفقیت حذف شد', 'success')
            return redirect('leave:userequest')
        else:
            messages.error(request, 'امکان حذف این درخواست  به دلیل تعیین وضعیت نهایی وجود ندارد ', 'warning')
            return redirect('leave:userequest')


class CheckUserRequest(LoginRequiredMixin, View):

    def get(self, request):
        if request.user.is_admin:
            middlemanager = User.objects.filter(is_MiddleManager=True)
            leave = Leave_Request.objects.filter(user__in=middlemanager, state='pending')
            return render(request, 'leave/check_request.html', context={"leave": leave})
        elif request.user.is_MiddleManager:
            employee = User.objects.filter(is_MiddleManager=False, is_admin=False)
            leave = Leave_Request.objects.filter(user__in=employee, state='pending')
            return render(request, 'leave/check_request.html', context={"leave": leave})
        else:
            messages.error(request, "امکان دسترسی به این صفحه برای شما وجود ندارد")
            return redirect("accounts:userhome")


class ShowUserRequest(LoginRequiredMixin, View):
    form_class = AdminReason

    def get(self, request, item_id):
        form = self.form_class
        leave = Leave_Request.objects.get(id=item_id)
        return render(request, 'leave/show_user_request.html', context={'leave': leave, 'form': form})

    def post(self, request, item_id):
        form = self.form_class(request.POST)
        leave = Leave_Request.objects.get(id=item_id)
        if form.is_valid():
            cd = form.cleaned_data
            leave.admin_reason = cd['admin_reason']
            leave.save()
            return redirect('leave:checkrequest')


class DeclineUserRequest(LoginRequiredMixin, View):

    def get(self, request, leave_id):
        leave = Leave_Request.objects.get(id=leave_id)
        leave.save()
        leave.state = 'decline'
        leave.save()
        messages.success(request, 'با درخواست مورد نظر موافقت نشد', 'success')
        return redirect('leave:checkrequest')


class ShowEmployee(LoginRequiredMixin, View):
    def setup(self, request, *args, **kwargs):
        if request.user.is_admin or request.user.is_MiddleManager:
            return super().setup(request, *args, **kwargs)
        else:
            return redirect('accounts:userhome')

    def get(self, request):
        if request.user.is_admin:
            user = User.objects.all()
            return render(request, 'leave/show_employee.html', context={'user': user})
        else:
            user_department_codes = request.user.department_code.values_list('department_code', flat=True)
            user = User.objects.filter(department_code__department_code__in=user_department_codes, is_admin=False,
                                       is_MiddleManager=False)
            return render(request, 'leave/show_employee.html', context={'user': user})


class ShowEmployeeDetails(LoginRequiredMixin, View):
    def setup(self, request, *args, **kwargs):
        if request.user.is_admin or request.user.is_MiddleManager:
            return super().setup(request, *args, **kwargs)
        else:
            return redirect('accounts:userhome')

    def get(self, request, userid):
        user = User.objects.get(user_id=userid)
        return render(request, 'leave/show_employee_details.html', context={"user": user})

    def post(self, request, userid):
        user = User.objects.get(user_id=userid)
        user.Full_name = request.POST.get('Full_name')

        user.number_of_month_leave_left = request.POST.get('number_of_month_leave_left')
        user.number_of_year_leave_left = request.POST.get('number_of_year_leave_left')
        user.number_of_sick_leave_left = request.POST.get('number_of_sick_leave_left')
        user.email = request.POST.get('email')
        user.user_phone = request.POST.get('user_phone')
        user.save()
        return redirect('leave:show_employee')
