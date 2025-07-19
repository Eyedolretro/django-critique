from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),  # page d’accueil

    path('signup/', views.signup, name='signup'),

    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('flux/', views.flux_view, name='flux'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),

    path('my_posts/', views.my_posts, name='my_posts'),

    path('create_ticket/', views.create_ticket, name='create_ticket'),
    path('create_review/<int:ticket_id>/', views.create_review, name='create_review'),
]
