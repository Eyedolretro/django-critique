from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .forms import SignupForm, TicketForm, ReviewForm
from .models import Ticket, Review, UserFollows

def home(request):
    if request.user.is_authenticated:
        return redirect('flux')
    return render(request, 'reviews/home.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('flux')
    else:
        form = SignupForm()
    return render(request, 'reviews/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('flux')
    else:
        form = AuthenticationForm()
    return render(request, 'reviews/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def flux_view(request):
    user = request.user
    followed_users = UserFollows.objects.filter(user=user).values_list('followed_user', flat=True)

    tickets = Ticket.objects.filter(
        user__in=followed_users
    ).order_by('-created_at')

    # Ajout des tickets de l'utilisateur lui-même
    tickets = tickets | Ticket.objects.filter(user=user)

    tickets = tickets.distinct().order_by('-created_at')

    reviews_prefetch = Review.objects.prefetch_related('responses').order_by('-created_at')
    tickets = tickets.prefetch_related(
        'reviews',  # Pour récupérer les reviews liées aux tickets
    )

    tickets_replied_to = Review.objects.filter(user=user).values_list('ticket_id', flat=True)

    return render(request, 'reviews/flux.html', {
        'tickets': tickets,
        'tickets_replied_to': tickets_replied_to,
    })

@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('flux')
    else:
        form = TicketForm()
    return render(request, 'reviews/create_ticket.html', {'form': form})

@login_required
def create_review(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('flux')
    else:
        form = ReviewForm()

    return render(request, 'reviews/create_review.html', {'form': form, 'ticket': ticket})

@login_required
def subscriptions(request):
    user = request.user
    followed_users = UserFollows.objects.filter(user=user).select_related('followed_user')
    return render(request, 'reviews/subscriptions.html', {'followed_users': followed_users})


@login_required
def my_posts(request):
    tickets = Ticket.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'reviews/my_posts.html', {'tickets': tickets})
