from django.urls import path
from . import views

urlpatterns = [
    # Page views
    path('',                  views.home,          name='home'),
    path('profile/',          views.profile,       name='profile'),
    path('styling/',          views.styling_page,  name='styling'),
    path('feedback/',         views.feedback,      name='feedback'),
    path('wardrobe/',         views.wardrobe,      name='wardrobe'),
    path('generate-outfit/',  views.generate_outfit, name='generate_outfit'),

    # API views
    path("api/profile/",                    views.profile_api,               name="profile_api"),
    path('api/weather/',      views.weather_api,   name='weather_api'),
    path('api/wardrobe/',     views.wardrobe_api,  name='wardrobe_api'),
    path('api/wardrobe/<int:item_id>/delete/', views.wardrobe_delete_api, name='wardrobe_delete'),
    path('api/save-outfit/',  views.save_outfit_api,  name='save_outfit'),
    path('recommend/',        views.recommend_outfits_api, name='recommend'),
    path("api/generate-tryon/",             views.generate_tryon_api,         name="generate_tryon_api"),
    path('api/upload-profile-image/',        views.upload_profile_image_api,       name='upload_profile_image'),
    path("api/generate-outfit-suggestions/", views.generate_outfit_suggestions, name="generate_outfit_suggestions"),
     path("api/generate-tryon-ai/", views.generate_tryon_ai, name="generate_tryon_ai"),
]