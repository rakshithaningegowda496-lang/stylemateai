from django.urls import path
from . import views

urlpatterns = [
    path('',                                       views.home,                  name='home'),
    path('profile/',                           views.profile,          name='profile'),
    path('styling/',                               views.styling_page,          name='styling'),
    path('tryon/',                                 views.tryon,                 name='tryon'),
    path('feedback/',                              views.feedback,              name='feedback'),
    path('wardrobe/',                              views.wardrobe,              name='wardrobe'),
    path('api/profile/',                           views.profile_api,           name='profile_api'),
    path('api/weather/',                           views.weather_api,           name='weather_api'),
    path('api/save-outfit/',                       views.save_outfit_api,       name='save_outfit'),
    path('api/wardrobe/',                          views.wardrobe_api,          name='wardrobe_api'),
    path('api/wardrobe/<int:item_id>/delete/',     views.wardrobe_delete_api,   name='wardrobe_delete'),
    path('recommend/',                             views.recommend_outfits_api, name='recommend'),
    path('generate-outfit/',                       views.generate_outfit,       name='generate_outfit'),
]