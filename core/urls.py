from django.urls import path
from .views import profile_api
from . import views

urlpatterns = [
path('', views.tryon, name='home'),        # homepage = try-on
path('profile/', views.profile, name='profile'),
path('tryon/', views.tryon, name='tryon'),
]

