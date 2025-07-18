from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Review, Ticket
from .forms import ReviewForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import TicketForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth import login, authenticate
from django.shortcuts import render
from .models import Ticket
from django.contrib.auth.models import User
from .models import Ticket
from django.db.models import Q
from django.http import HttpResponse
from .forms import ArticleForm
from django.contrib.auth.decorators import login_required
from .models import Ticket, Comment, UserFollows
from itertools import chain
from django.utils import timezone
from .models import Ticket, Review, UserFollows
from django.shortcuts import redirect
from .forms import FollowUserForm
from .models import UserFollows
from django.contrib import messages
from .forms import FollowForm
from django.shortcuts import get_object_or_404
from .models import Review, Response
from .forms import ResponseForm
from .models import Review
from .models import Ticket, Review, Response, UserFollows
from .models import Article
from django.db.models import Prefetch










@login_required
def home(request):
    tickets = Ticket.objects.filter(user=request.user)
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
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'reviews/signup.html', {'form': form})


 







@login_required
def create_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user  # associer l'user connecté
            ticket.save()
            return redirect('home')  # ou vers la page souhaitée après création
    else:
        form = TicketForm()
    return render(request, 'reviews/create_ticket.html', {'form': form})







def search_user(request):
    query = request.GET.get('query', '')
    results = []

    if query:
        results = Ticket.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(user__username__icontains=query)
        )

    return render(request, 'reviews/search_user.html', {'results': results, 'query': query})




def search_user_by_ticket(request):
    query = request.GET.get('query', '')
    results = []

    if query:
        results = Ticket.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(user__username__icontains=query)
        )

    return render(request, 'reviews/search_user.html', {'results': results, 'query': query})




@login_required
def publish_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            Article.objects.create(content=content, author=request.user)
            messages.success(request, "Article publié !")
            return redirect('mes_articles')
    else:
        form = ArticleForm()
    
    return render(request, 'reviews/publish_article.html', {'form': form})




@login_required
def user_feed(request):
    # Récupérer les utilisateurs suivis
    followed_users = UserFollows.objects.filter(user=request.user).values_list('followed_user', flat=True)

    # Récupérer les tickets et commentaires des suivis
    tickets = Ticket.objects.filter(user__in=followed_users)
    comments = Comment.objects.filter(user__in=followed_users)

    # Fusionner et trier par date
    feed_items = sorted(
        chain(tickets, comments),
        key=lambda instance: instance.created_at,
        reverse=True
    )

    return render(request, 'reviews/feed.html', {'feed_items': feed_items})



@login_required
def followed_users_feed(request):
    user = request.user
    followed_users = UserFollows.objects.filter(user=user).values_list('followed_user', flat=True)

    tickets = Ticket.objects.filter(user__in=followed_users)
    reviews = Review.objects.filter(user__in=followed_users)
    responses = Response.objects.filter(responder__in=followed_users)

    # on ajoute un champ virtuel "type" pour distinguer dans le template
    for obj in tickets:
        obj.feed_type = "ticket"
    for obj in reviews:
        obj.feed_type = "review"
    for obj in responses:
        obj.feed_type = "response"

    items = sorted(
        chain(tickets, reviews, responses),
        key=lambda item: item.created_at,
        reverse=True
    )

    # gestion du formulaire de réponse à une Review
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            review_id = request.POST.get('review_id')
            review = get_object_or_404(Review, pk=review_id)
            response = form.save(commit=False)
            response.review = review
            response.responder = user
            response.save()
            return redirect('followed_users_feed')
    else:
        form = ResponseForm()

    context = {
        'items': items,
        'form': form,
        'user': user
    }
    return render(request, 'reviews/followed_users_feed.html', context)


    # Gestion du formulaire de réponse (POST)
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            review_id = request.POST.get('review_id')
            review = get_object_or_404(Review, pk=review_id)
            response = form.save(commit=False)
            response.review = review
            response.responder = user
            response.save()
            return redirect('followed_users_feed')
    else:
        form = ResponseForm()

    context = {
        'items': items,
        'form': form,
        'user': user
    }
    return render(request, 'reviews/followed_users_feed.html', context)

@login_required
def follow_user(request):
    if request.method == 'POST':
        form = FollowUserForm(request.POST)
        if form.is_valid():
            followed_user = form.cleaned_data['username']
            if followed_user != request.user:
                UserFollows.objects.get_or_create(user=request.user, followed_user=followed_user)
            return redirect('followed_users_feed')
    else:
        form = FollowUserForm()
    return render(request, 'reviews/follow_user.html', {'form': form})




@login_required
def subscriptions_view(request):
    user = request.user
    following = UserFollows.objects.filter(user=user)
    followers = UserFollows.objects.filter(followed_user=user)
    return render(request, 'reviews/subscriptions.html', {
        'following': following,
        'followers': followers,
    })



@login_required
def subscriptions_view(request):
    user = request.user

    # Utilisateurs que je suis
    following = UserFollows.objects.filter(user=user)

    # Utilisateurs suivis (juste les utilisateurs, pas les objets UserFollows)
    followed_users = [f.followed_user for f in following]

    # Pour chaque utilisateur que je suis, on récupère ses abonnés
    followers_of_followed = {
        u: UserFollows.objects.filter(followed_user=u) for u in followed_users
    }

    context = {
        'following': followed_users,  # liste de User
        'followers_of_followed': followers_of_followed,  # dict user -> [UserFollows]
    }
    return render(request, 'reviews/subscriptions.html', context)



@login_required
def unsubscribe_view(request, follow_id):
    follow = get_object_or_404(UserFollows, id=follow_id, user=request.user)

    if request.method == 'POST':
        follow.delete()
        messages.success(request, f"Vous vous êtes désabonné de {follow.followed_user.username}.")

    return redirect('subscriptions')




@login_required
def create_review_for_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('flux')  # ou autre page souhaitée
    else:
        form = ReviewForm()

    return render(request, 'reviews/create_review.html', {
        'form': form,
        'ticket': ticket
    })
    



@login_required
def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    responses = review.responses.all()
    
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.review = review
            response.responder = request.user
            response.save()
            return redirect('review_detail', pk=review.pk)
    else:
        form = ResponseForm()

    return render(request, 'reviews/review_detail.html', {
        'review': review,
        'responses': responses,
        'form': form,
    })



def review_list(request):
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'reviews/review_list.html', {'reviews': reviews})



def feed_view(request):
    feed = get_user_feed(request.user)  # exemple
    form = ResponseForm()
    return render(request, 'followed_users_feed.html', {
        'feed': feed,
        'form': form,
    })

def mes_contributions(request):
    user = request.user
    tickets = Ticket.objects.filter(user=user).order_by('-created_at')
    publications = Review.objects.filter(user=user).order_by('-created_at')
    articles = Article.objects.filter(author=user).order_by('-created_at')  # <--- ajout

    return render(request, 'reviews/mes_contributions.html', {
        'tickets': tickets,
        'publications': publications,
        'articles': articles,  # <--- ajout
    })



@login_required
def mes_articles(request):
    articles = Article.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'reviews/mes_articles.html', {'articles': articles})



@login_required
def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id, author=request.user)

    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, "Article modifié avec succès.")
            return redirect('mes_contributions')
    else:
        form = ArticleForm(instance=article)

    return render(request, 'reviews/edit_article.html', {'form': form})




@login_required
def delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id, author=request.user)

    if request.method == "POST":
        article.delete()
        messages.success(request, "Article supprimé.")
        return redirect('mes_contributions')

    return render(request, 'reviews/delete_article.html', {'article': article})



@login_required
def my_posts(request):
    user = request.user

    reviews = Review.objects.filter(user=user).prefetch_related(
        Prefetch('responses', queryset=Response.objects.select_related('responder'))
    )

    tickets = Ticket.objects.filter(user=user)

    context = {
        'reviews': reviews,
        'tickets': tickets,
    }

    return render(request, 'reviews/my_posts.html', context)