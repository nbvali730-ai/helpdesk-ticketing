from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.utils import timezone

from .forms import TicketForm, TicketMessageForm, CustomUserCreationForm
from .models import Ticket, UserProfile


@login_required
def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.status = 'OPEN'
            ticket.department = 'IT'
            ticket.save()
            return redirect('ticket_list')
    else:
        form = TicketForm()

    return render(request, 'tickets/ticket_create.html', {'form': form})


@login_required
def it_ticket_list(request):
    # چک کردن دسترسی پنل IT
    if not hasattr(request.user, 'userprofile') or not request.user.userprofile.is_it_support:
        return redirect('ticket_list')

    active_tickets = Ticket.objects.filter(
        department='IT',
        status='OPEN'
    ).order_by('-created_at')

    resolved_tickets = Ticket.objects.filter(
        department='IT',
        status='RESOLVED'
    ).order_by('-updated_at')

    return render(request, 'tickets/it_ticket_list.html', {
        'tickets': active_tickets,
        'resolved_tickets': resolved_tickets
    })


@login_required
def ticket_list(request):
    tickets = Ticket.objects.filter(
        created_by=request.user
    ).order_by('-created_at')

    return render(request, 'tickets/ticket_list.html', {'tickets': tickets})


@login_required
def ticket_detail(request, pk=None, ticket_id=None):
    identifier = pk or ticket_id
    ticket = get_object_or_404(Ticket, pk=identifier)

    messages = ticket.messages.all().order_by('created_at')

    if request.method == 'POST':
        form = TicketMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.ticket = ticket
            message.author = request.user
            message.save()

            ticket.updated_at = timezone.now()
            ticket.save()

            return redirect('ticket_detail', pk=ticket.pk)
    else:
        form = TicketMessageForm()

    return render(request, 'tickets/ticket_detail.html', {
        'ticket': ticket,
        'messages': messages,
        'form': form
    })


@login_required
def resolve_ticket(request, ticket_id):
    if request.method != 'POST':
        return redirect('it_ticket_list')

    ticket = get_object_or_404(Ticket, id=ticket_id)

    if not hasattr(request.user, 'userprofile') or not request.user.userprofile.is_it_support:
        return redirect('ticket_list')

    ticket.status = 'RESOLVED'
    ticket.updated_at = timezone.now()
    ticket.save()

    return redirect('it_ticket_list')


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # ایجاد پروفایل کاربر
            UserProfile.objects.get_or_create(
                user=user,
                full_name=form.cleaned_data.get('full_name'),
                gender=form.cleaned_data.get('gender'),
                work_location=form.cleaned_data.get('work_location'),
                job_title=form.cleaned_data.get('job_title')
            )

            login(request, user)
            return redirect("ticket_list")
    else:
        form = CustomUserCreationForm()

    return render(request, "registration/signup.html", {"form": form})
