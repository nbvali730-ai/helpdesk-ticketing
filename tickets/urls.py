from django.urls import path
from . import views

urlpatterns = [
    path("", views.ticket_list, name="ticket_list"),
    path("new/", views.ticket_create, name="ticket_create"),
    path("<int:pk>/", views.ticket_detail, name="ticket_detail"),
    path("<int:ticket_id>/resolve/", views.resolve_ticket, name="resolve_ticket"),
    path("it-panel/", views.it_ticket_list, name="it_ticket_list"),
    path("signup/", views.signup, name="signup"),
    # دیگر هیچ مسیر مربوط به accounts/login یا accounts/logout در اینجا نباید باشد.
]
