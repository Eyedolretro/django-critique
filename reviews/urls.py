from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),  # 👈 ajoute cette ligne
    path('review/<int:ticket_pk>/create/', views.CreateReviewView.as_view(), name='create_review'),
    path('ticket/create/', views.create_ticket, name='create_ticket'),
]
