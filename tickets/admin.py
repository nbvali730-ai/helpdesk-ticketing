# tickets/admin.py

from django.contrib import admin
from .models import Ticket, TicketMessage, UserProfile # مدل‌هایی که می‌خواهید در پنل ادمین نمایش دهید را اینجا import کنید

# Register your models here.
admin.site.register(Ticket)
admin.site.register(TicketMessage)
admin.site.register(UserProfile)
