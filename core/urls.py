from django.urls import path
from . import views

urlpatterns = [

    # Home / Welcome Page
    path('', views.profile_page, name='profile'),

    # Save Profile
    path('save-profile/', views.save_profile, name='save_profile'),

    # Other Pages
    path('styling/', views.styling_page, name='styling'),
    path('tryon/', views.tryon, name='tryon'),
    path('feedback/', views.feedback, name='feedback'),
    path('wardrobe/', views.wardrobe, name='wardrobe'),

    # AI Outfit Generator
    path('generate-outfit/', views.generate_outfit, name='generate_outfit'),

]