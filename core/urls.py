from django.urls import path
<<<<<<< HEAD
from . import views

urlpatterns = [
    # Pages
    path('', views.home, name='home'),
   
    path('styling/', views.styling_page, name='styling'),

    # APIs
    path('api/profile/', views.profile_api),
    path('api/weather/', views.weather_api),
    path('api/save-outfit/', views.save_outfit_api),
]
def homepage(request):
    return render(request, 'home.html')
=======
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
>>>>>>> 9279c106d7854342e64f690bf8c8b20f47c21ffa
