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
    path('publish/', views.publish_article, name='publish_article'),
    path('flux/', views.followed_users_feed, name='followed_users_feed'),
    path('follow/', views.follow_user, name='follow_user'),
    path('subscriptions/', views.subscriptions_view, name='subscriptions'),
    path('unsubscribe/<int:follow_id>/', views.unsubscribe_view, name='unsubscribe'),
    path('ticket/<int:ticket_id>/review/', views.create_review_for_ticket, name='create_review'),
    path('review/<int:pk>/', views.review_detail, name='review_detail'),
    path('reviews/', views.review_list, name='review_list'),
    path('mes-contributions/', views.mes_contributions, name='mes_contributions'),
    path('publier-article/', views.publish_article, name='publish_article'),
    path('mes-articles/', views.mes_articles, name='mes_articles'),
]






