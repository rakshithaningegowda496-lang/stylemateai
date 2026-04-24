from django.urls import path
from .views import profile_api

urlpatterns = [
    path('api/profile/', profile_api),
]