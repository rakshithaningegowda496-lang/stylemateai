from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile_page),
    path('profile/', views.profile_api),
    path('analyze/', views.analyze_image),
]