from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('user_id', "user_phone", "Full_name", 'is_admin', 'is_MiddleManager', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password1') and cd.get('password2') and cd.get("password1") != cd.get("password2"):
            raise ValidationError("passwords dont match")
        return cd.get("password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text="you can change password using <a href= \"../password/\"> this form </a>")

    class Meta:
        fields = ("user_id", "user_phone", "Full_name", "password", "last_login", 'email')


class UserLogin(forms.Form):
    user_id = forms.CharField(max_length=10)
    password = forms.CharField(max_length=250, widget=forms.PasswordInput)


class UserRegisterForm(forms.Form):

    user_id = forms.CharField(max_length=10,
                                      label="کد کاربری",
                                      widget=forms.TextInput(attrs={'placeholder': 'کد کاربری', 'style': 'background: transparent;', 'class': 'form-control col-md-4'}))

    user_phone = forms.CharField(max_length=11,
                                 label="شماره تماس",
                                      widget=forms.TextInput(attrs={'placeholder': 'شماره تماس', 'style': 'background: transparent;', 'class': 'form-control col-md-4'}))

    Full_name = forms.CharField(max_length=50,
                                label="نام و نام خانوادگی",
                                      widget=forms.TextInput(attrs={'placeholder': 'نام و نام خانوادگی', 'style': 'background: transparent;', 'class': 'form-control col-md-4'}))

    password = forms.CharField(label="گذروازه",
                               widget=forms.PasswordInput(attrs={'placeholder': 'گذرواژه', 'style': 'background: transparent;', 'class': 'form-control col-md-4'}))

    email = forms.EmailField(label="ایمیل",
                               widget=forms.TextInput(attrs={'placeholder': 'ایمیل', 'style': 'background: transparent;', 'class': 'form-control col-md-4'}))


class UserChangePassword(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_confirm_password(self):
        pass1 = self.cleaned_data['password']
        pass2 = self.cleaned_data['confirm_password']
        if pass1 and pass2 and pass1 == pass2:
            return pass1
        else:
            raise ValidationError('password must be match')


class AddDepartmentForm(forms.Form):
    # department_code = forms.CharField(max_length=250)
    department_name = forms.CharField(max_length=50,
                                      label="نام دپارتمان",
                                      widget=forms.TextInput(attrs={'placeholder': 'نام دپارتمان', 'style': 'background: transparent;', 'class': 'form-control col-md-4'}))


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()


class enter_phone(forms.Form):
    phone = forms.CharField(max_length=11,
                            label="شماره تماس:",
                            widget=forms.TextInput(attrs={'placeholder': 'شماره تماس را وارد کنید', 'style': 'background: transparent;', 'class': 'form-control col-md-4'}))
