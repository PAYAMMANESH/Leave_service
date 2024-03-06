from .models import Leave_Request
from django import forms



class AddUserLeaveRequestForm(forms.ModelForm):
    class Meta:
        model = Leave_Request
        fields = ('Leave_type', 'Leave_type_type', 'from_day', 'to_day', 'from_hour', 'to_hour', 'Reason', 'work_day')

    def __init__(self, *args, **kwargs):
        super(AddUserLeaveRequestForm, self).__init__(*args, **kwargs)
        self.fields['from_day'].widget.attrs['placeholder'] = 'روز-ماه-سال'
        self.fields['to_day'].widget.attrs['placeholder'] = 'روز-ماه-سال'
        self.fields['from_hour'].widget.attrs['placeholder'] = 'دقیقه:ساعت'
        self.fields['to_hour'].widget.attrs['placeholder'] = 'دقیقه:ساعت'

        self.fields['Leave_type'].label = 'نوع مرخصی'
        self.fields['Leave_type_type'].label = 'مدت زمان'
        self.fields['from_day'].label = 'تاریخ شروع'
        self.fields['to_day'].label = 'تاریخ پایان'
        self.fields['from_hour'].label = 'ساعت شروع'
        self.fields['to_hour'].label = 'ساعت پایان'
        self.fields['Reason'].label = 'دلیل مرخصی'
        self.fields['work_day'].label = 'روز کاری'
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control col-md-3'
        if self.instance.Leave_type_type == 'daily':
            self.fields['from_hour'].widget.attrs['style'] = 'display:none;'
            self.fields['to_hour'].widget.attrs['style'] = 'display:none;'



class AdminReason(forms.ModelForm):
    class Meta:
        model = Leave_Request
        fields = ('admin_reason',)

    def __init__(self, *args, **kwargs):
        super(AdminReason, self).__init__(*args, **kwargs)

        # Change the label of the admin_reason field
        self.fields['admin_reason'].label = 'توضیحات مدیر'

        # Add the Bootstrap form-control class and make the field transparent
        self.fields['admin_reason'].widget.attrs.update({
            'class': 'form-control',
            'style': 'background: transparent;color: white;font-size: 15px',

        })