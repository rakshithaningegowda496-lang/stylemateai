from django.urls import path
<<<<<<< HEAD
from .views import profile_api
from . import views

urlpatterns = [
path('', views.tryon, name='home'),        # homepage = try-on
path('profile/', views.profile, name='profile'),
path('tryon/', views.tryon, name='tryon'),
]

=======
from .views import profile_api ,generate_outfit ,styling_page 


urlpatterns = [
    path('api/profile/', profile_api),
    path('generate-outfit/', generate_outfit),
    path('styling/', styling_page)
]
>>>>>>> 02e436f84cf7aeb21df953b9fc65d8b533f4d188
