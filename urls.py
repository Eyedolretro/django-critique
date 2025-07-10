from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', views.home, name='home'),  # page d'accueil / tickets
    path('login/', auth_views.LoginView.as_view(template_name='myapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('ticket/create/', views.create_ticket, name='create_ticket'),
    path('admin/', admin.site.urls),
    path('', include('critiquehub.urls')),
    path('admin/', admin.site.urls),
    path('', include('reviews.urls')),  # Assurez-vous que les URLs de l'app sont bien incluses
    path('accounts/', include('django.contrib.auth.urls')),  # <-- IMPORTANT !
]





