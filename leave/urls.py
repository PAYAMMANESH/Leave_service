from django.urls import path
from . import views

app_name = 'leave'

urlpatterns = [
    path('request/', views.UserRequest.as_view(), name='userequest'),
    path('add_request/', views.AddUserLeaveRequest.as_view(), name='addleave'),
    path('add_employee_request/', views.AddEmployeeLeaveRequest.as_view(), name='add_employee_leave'),
    path('add_accept_leave/<str:user_id>', views.AddAndAcceptLeave.as_view(), name='add_and_accept_leave'),
    path('request_detail/<int:re_id>/', views.UserRequestDetail.as_view(), name='requestdetail'),
    path('request_delete/<int:re_id>/', views.UserRequestDelete.as_view(), name='requestdelete'),
    path('check_request/', views.CheckUserRequest.as_view(), name='checkrequest'),
    path('show_user_request/<int:item_id>', views.ShowUserRequest.as_view(), name="show_user_request"),
    path('accept_request/<int:leave_id>', views.AcceptUserRequest.as_view(), name='accept_request'),
    path('decline_request/<int:leave_id>', views.DeclineUserRequest.as_view(), name='decline_request'),
    path('show_employee/', views.ShowEmployee.as_view(), name='show_employee'),
    path('show_employee_detail/<str:userid>/', views.ShowEmployeeDetails.as_view(), name='show_employee_detail')
]
