"""
URL configuration for style project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

def styling_page(request):
    return render(request, "styling.html")

urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path('', include('core.urls')),   # all pages handled in core
]
=======

    path('', profile_page, name='profile'),   # ✅ add name
    path('styling/', styling_page, name='styling'),  # ✅ ADD THIS LINE

    path('', include('core.urls')),
]
>>>>>>> 02e436f84cf7aeb21df953b9fc65d8b533f4d188
