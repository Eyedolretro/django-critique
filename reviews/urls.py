from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),  # 👈 ajoute cette ligne
    path('review/<int:ticket_pk>/create/', views.CreateReviewView.as_view(), name='create_review'),
    path('ticket/create/', views.create_ticket, name='create_ticket'),
    path('create_ticket/', views.create_ticket, name='create_ticket'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('search-user/', views.search_user_by_ticket, name='search_user'),
]






