from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Ticket
from django import forms

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description']

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # connecte directement après inscription
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'myapp/signup.html', {'form': form})

@login_required
def home(request):
    tickets = Ticket.objects.filter(user=request.user)
    return render(request, 'myapp/home.html', {'tickets': tickets})

@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')
    else:
        form = TicketForm()
    return render(request, 'myapp/create_ticket.html', {'form': form})
