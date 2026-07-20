from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test
# اطمینان حاصل کنید که UserProfile از models.py وارد شده است
from .models import UserProfile


def is_it_support_user(user):
    """
    این تابع چک می‌کند که آیا کاربر فعلی، کاربری با نقش پشتیبانی IT است یا خیر.
    """
    if user.is_authenticated:
        try:
            # تلاش برای یافتن پروفایل کاربر
            user_profile = UserProfile.objects.get(user=user)
            # اگر پروفایل پیدا شد، وضعیت is_it_support را برمی‌گرداند
            return user_profile.is_it_support
        except UserProfile.DoesNotExist:
            # اگر پروفایلی برای کاربر وجود نداشت، به معنی عدم دسترسی است
            return False
    # اگر کاربر لاگین نکرده باشد، دسترسی ندارد
    return False


# این خط، دکوریتوری را ایجاد می‌کند که تابع is_it_support_user را فراخوانی می‌کند
# و اگر تابع False برگرداند، کاربر را به صفحه لاگین هدایت می‌کند (login_url را می‌توانید تغییر دهید)
it_support_required = user_passes_test(is_it_support_user, login_url='/accounts/login/')
