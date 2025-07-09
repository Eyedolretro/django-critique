from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Review, Ticket
from .forms import ReviewForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def home(request):
    tickets = Ticket.objects.all()
    return render(request, 'reviews/home.html', {'tickets': tickets})

class CreateReviewView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/create_review.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.ticket = get_object_or_404(Ticket, pk=self.kwargs['ticket_pk'])
        return super().form_valid(form)





def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige vers la page de connexion après inscription
    else:
        form = UserCreationForm()
    return render(request, 'reviews/signup.html', {'form': form})

