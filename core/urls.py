from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('styling/', views.styling_page, name='styling'),
    path('tryon/', views.tryon, name='tryon'),
    path('feedback/', views.feedback, name='feedback'),
    path('wardrobe/', views.wardrobe, name='wardrobe'),
    # ← ADD THIS
    path('api/profile/', views.profile_api),
    path('api/weather/', views.weather_api),
    path('api/save-outfit/', views.save_outfit_api),
    path('generate-outfit/', views.generate_outfit),
]