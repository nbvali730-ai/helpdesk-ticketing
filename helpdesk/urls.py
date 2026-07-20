from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views # این خط را نگه دارید

urlpatterns = [
    path('admin/', admin.site.urls),

    # مسیرهای احراز هویت (Login/Logout) - اینها باید در اینجا باشند
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/tickets/'), name='logout'),

    # مسیرهای اپلیکیشن tickets - این خط مهم است
    path('tickets/', include('tickets.urls')),

    # هدایت مسیر ریشه به tickets
    path('', RedirectView.as_view(url='/tickets/', permanent=False)),
]
