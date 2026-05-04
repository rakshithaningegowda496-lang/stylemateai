from django.urls import path
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