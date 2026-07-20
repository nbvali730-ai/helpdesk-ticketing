from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Ticket, TicketMessage


# فرم ثبت‌نام
class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, required=True, label="نام و نام خانوادگی")
    gender = forms.ChoiceField(choices=UserProfile.GENDER_CHOICES, label="جنسیت")
    workplace = forms.CharField(max_length=255, required=False, label="محل کار")
    job_title = forms.CharField(max_length=255, required=False, label="سمت شغلی")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('full_name', 'gender', 'workplace', 'job_title')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # استایل تم تیره برای همه فیلدها
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control bg-dark text-white border-secondary'
            })

        # اصلاح کلاس برای select جنسیت
        self.fields['gender'].widget.attrs.update({
            'class': 'form-select bg-dark text-white border-secondary'
        })

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()

            UserProfile.objects.update_or_create(
                user=user,
                defaults={
                    'full_name': self.cleaned_data.get('full_name'),
                    'gender': self.cleaned_data.get('gender'),
                    'workplace': self.cleaned_data.get('workplace'),
                    'job_title': self.cleaned_data.get('job_title'),
                }
            )

        return user


# فرم ایجاد تیکت (بدون دپارتمان)
class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'priority']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-white border-secondary'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-white border-secondary',
                'rows': 4
            }),

            'priority': forms.Select(attrs={
                'class': 'form-select bg-dark text-white border-secondary'
            }),
        }


# فرم ارسال پیام در تیکت
class TicketMessageForm(forms.ModelForm):

    class Meta:
        model = TicketMessage
        fields = ['body']

        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-white border-secondary',
                'rows': 3,
                'placeholder': 'پیام خود را اینجا بنویسید...'
            }),
        }
