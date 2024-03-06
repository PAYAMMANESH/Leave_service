from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    #path('', views.HomePage.as_view(), name='home'),
    path('home/', views.homepage.as_view(), name='userhome'),
    path('change/<str:userid>/', views.ChangeProf.as_view(), name='userchange'),
    path('', views.UserLogin.as_view(), name='userlogin'),
    path("verify/", views.UserVerifyPhone.as_view(), name="verify_phone"),
    path('logout/', views.UserLogout.as_view(), name='userlogout'),
    path('register/<str:dp_code>', views.UserRegister.as_view(), name='userregister'),
    path('changepassword', views.UserChangePass.as_view(), name='changepass'),
    path('departman/', views.DepartmanView.as_view(), name='departman'),
    path('add_departman/', views.AddDepartmanView.as_view(), name='Add_departman'),
    path('departman/detail/<str:dp_code>/', views.DepartmanDetailview.as_view(), name='departman_detail'),
    path('departman/delete/<str:dp_code>/', views.DepartamnDelete.as_view(), name='departman_delete'),
    path('manager/register/<str:dp_code>', views.ManagerRegister.as_view(), name='managerregister'),
    path('show_employee/<str:dp_code>', views.ShowEmployee.as_view(), name='show_employee'),
    path('show_Manager/<str:dp_code>', views.ShowManager.as_view(), name='show_manager'),
    path('add_old_employee/<str:userid>/<str:dp_code>/', views.AddOldEmployee.as_view(), name="add_old_employee"),
    path('add_old_Manager/<str:user_id>/<str:dp_code>/', views.AddOldManager.as_view(), name="add_old_manager"),
    path('show_department_employee/<str:dp_code>/', views.ShowDepartmentEmployee.as_view(), name='department_employee'),
    path('delete_employee/<str:user_id>/<str:dp_code>/', views.DeleteEmployee.as_view(), name='delete_employee'),
    path('forgot_password/', views.ForgotPassword.as_view(), name='forgot_pass'),
    path('verify_code/<str:phone>', views.VerifyForgotPassCode.as_view(), name='verify_forgot_pass_code'),
    path('change_pass/<str:userid>', views.UserforgotPass.as_view(), name='password_reset_complete')


]
