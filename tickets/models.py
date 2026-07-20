from django.db import models
from django.contrib.auth.models import User


class Ticket(models.Model):

    class Status(models.TextChoices):
        OPEN = 'OPEN', 'باز'
        IN_PROGRESS = 'IN_PROGRESS', 'در حال بررسی'
        RESOLVED = 'RESOLVED', 'حل شده'
        CLOSED = 'CLOSED', 'بسته شده'

    class Department(models.TextChoices):
        IT = 'IT', 'فناوری اطلاعات'
        MGMT = 'MGMT', 'مدیریت'

    class Priority(models.TextChoices):
        LOW = 'LOW', 'کم'
        MEDIUM = 'MEDIUM', 'متوسط'
        HIGH = 'HIGH', 'فوری'

    title = models.CharField(max_length=200, verbose_name="عنوان")

    description = models.TextField(verbose_name="توضیحات")

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tickets",
        verbose_name="ایجاد کننده"
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tickets",
        verbose_name="ارجاع به"
    )

    department = models.CharField(
        max_length=10,
        choices=Department.choices,
        default=Department.IT,
        verbose_name="واحد"
    )

    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
        verbose_name="اولویت"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN,
        verbose_name="وضعیت"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class TicketMessage(models.Model):

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    body = models.TextField(verbose_name="متن پیام")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.author}"


class UserProfile(models.Model):

    GENDER_CHOICES = [
        ('male', 'مرد'),
        ('female', 'زن'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True,
        null=True,
        verbose_name="جنسیت"
    )

    is_it_support = models.BooleanField(
        default=False,
        verbose_name="پشتیبان IT"
    )

    full_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="نام کامل"
    )

    job_title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="سمت"
    )

    def __str__(self):
        return self.user.username
