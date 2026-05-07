from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Profile, UserProfile
from .ml_model import predict_outfit
import json
import requests


def home(request):
    return render(request, 'home.html')


# 🔹 PAGES
def styling_page(request):
    return render(request, "styling.html")


def tryon(request):
    profile_exists = UserProfile.objects.exists()
    return render(request, 'tryon.html', {'profile_exists': profile_exists})


def profile(request):
    if request.method == 'POST':
        skin_tone = request.POST.get('skin_tone')
        skin_type = request.POST.get('skin_type')
        body_type = request.POST.get('body_type')
        gender = request.POST.get('gender')
        location = request.POST.get('location')

        UserProfile.objects.create(
            skin_tone=skin_tone,
            skin_type=skin_type,
            body_type=body_type,
            gender=gender,
            location=location
        )
        return redirect('tryon')

    return render(request, 'profile.html')


# 🔹 PROFILE API
@csrf_exempt
def profile_api(request):
    profile, created = Profile.objects.get_or_create(id=1)

    if request.method == "GET":
        return JsonResponse({
            "name":      profile.name,
            "skin_tone": profile.skin_tone,
            "skin_type": profile.skin_type,
            "body_type": profile.body_type,
            "gender":    profile.gender,
            "location":  profile.location,
        })

    if request.method == "POST":
        data = json.loads(request.body)
        profile.skin_tone = data.get("skin_tone")
        profile.skin_type = data.get("skin_type")
        profile.body_type = data.get("body_type")
        profile.gender    = data.get("gender")
        profile.location  = data.get("location")
        profile.save()
        return JsonResponse({"status": "saved"})


# 🔹 GENERATE OUTFIT (ML)
@csrf_exempt
def generate_outfit(request):
    if request.method == "POST":
        data     = json.loads(request.body)
        occasion = data.get("occasion")
        mood     = data.get("mood")
        outfit   = predict_outfit(occasion, mood)
        return JsonResponse({"outfit": outfit})
    return JsonResponse({"error": "Only POST allowed"})


# 🔹 WEATHER API
@csrf_exempt
def weather_api(request):
    location = request.GET.get("location", "").strip()
    if not location:
        return JsonResponse({"error": "Location is required"}, status=400)

    api_key = settings.WEATHER_API_KEY
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={location}&appid={api_key}&units=metric"
    )

    try:
        res  = requests.get(url, timeout=5)
        data = res.json()

        if data.get("cod") != 200:
            return JsonResponse({"error": "City not found"}, status=404)

        weather = {
            "location":    data["name"] + ", " + data["sys"]["country"],
            "temperature": round(data["main"]["temp"]),
            "feels_like":  round(data["main"]["feels_like"]),
            "condition":   data["weather"][0]["main"],
            "description": data["weather"][0]["description"].title(),
            "humidity":    data["main"]["humidity"],
            "wind_speed":  round(data["wind"]["speed"] * 3.6, 1),
            "icon":        data["weather"][0]["icon"],
        }

        profile, _ = Profile.objects.get_or_create(id=1)
        from .models import WeatherLog
        WeatherLog.objects.create(
            profile=profile,
            location=weather["location"],
            temperature=weather["temperature"],
            condition=weather["condition"],
            humidity=weather["humidity"],
            wind_speed=weather["wind_speed"],
        )

        return JsonResponse(weather)

    except requests.exceptions.Timeout:
        return JsonResponse({"error": "Weather service timeout"}, status=503)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# 🔹 SAVE OUTFIT HISTORY
@csrf_exempt
def save_outfit_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        profile, _ = Profile.objects.get_or_create(id=1)
        from .models import OutfitHistory
        OutfitHistory.objects.create(
            profile=profile,
            occasion=data.get("occasion", ""),
            profession=data.get("profession", ""),
            mood=data.get("mood", ""),
            colors_used=data.get("colors_used", ""),
            outfit_json=json.dumps(data.get("outfits", [])),
            location=data.get("location", ""),
            temperature=data.get("temperature"),
            condition=data.get("condition", ""),
        )
        return JsonResponse({"status": "saved"})
    return JsonResponse({"error": "POST required"}, status=405)
def home(request):
    return render(request, 'tryon.html')
def feedback(request):
    return render(request, 'feedback.html')
def wardrobe(request):
    return render(request, 'wardrobe.html')

