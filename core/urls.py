from django.urls import path
from .views import profile_page
from . import views

urlpatterns = [
    path('', profile_page, name='profile'),
    path('styling/', views.styling_page, name='styling'),
    path('tryon/', views.tryon, name='tryon'),
    path('feedback/', views.feedback, name='feedback'),
    path('wardrobe/', views.wardrobe, name='wardrobe'),

    # AI Outfit Generator
    path('generate-outfit/', views.generate_outfit, name='generate_outfit'),

]