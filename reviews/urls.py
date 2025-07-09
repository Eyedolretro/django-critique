from django.urls import path
from .views import home, CreateReviewView

urlpatterns = [
    path('', home, name='home'),
    path('review/<int:ticket_pk>/create/', CreateReviewView.as_view(), name='create_review'),
]

