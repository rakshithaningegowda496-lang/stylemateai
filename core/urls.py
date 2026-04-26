from django.urls import path
from .views import profile_api ,generate_outfit ,styling_page 


urlpatterns = [
    path('api/profile/', profile_api),
    path('generate-outfit/', generate_outfit),
    path('styling/', styling_page)
]