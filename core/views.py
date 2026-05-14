from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Profile, UserProfile, WardrobeItem
import json
import requests

def home(request):
    return render(request, 'home.html')
GENDER_CHOICES = ['Female', 'Male', 'Non-binary', 'Prefer Not To Say']

def profile_page(request):
    step = int(request.POST.get("step", 1))
    step = 1

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "continue":
            step = 2

        elif action == "back":
            step = 1

    context = {
        "step": step,
    }
        

    return render(request, 'profile.html', context)


# Styling Page
def styling_page(request):
    return render(request, "styling.html")
    return render(request, 'styling.html')


# Try On Page
def tryon(request):
    return render(request, "tryon.html")

def feedback(request):
    return render(request, 'feedback.html')

# Feedback Page
def feedback(request):
    return render(request, "feedback.html")


# Wardrobe Page
def wardrobe(request):
    return render(request, "wardrobe.html")


# API - Profile
def profile_api(request):

    return JsonResponse({
        "message": "Profile API working"
    })


# API - Weather
def weather_api(request):

    return JsonResponse({
        "weather": "Sunny"
    })


# API - Save Outfit
def save_outfit_api(request):

    return JsonResponse({
        "status": "saved"
    })


# AI Outfit Generator
def generate_outfit(request):

    return JsonResponse({
        "outfit": "Casual Jeans + White Shirt"
    })
def profile(request):
    if request.method == 'POST':
        UserProfile.objects.create(
            skin_tone=request.POST.get('skin_tone'),
            skin_type=request.POST.get('skin_type'),
            body_type=request.POST.get('body_type'),
            gender=request.POST.get('gender'),
            location=request.POST.get('location'),
        )
        return redirect('tryon')
    return render(request, 'profile.html')

def wardrobe(request):
    items = WardrobeItem.objects.all()
    return render(request, 'wardrobe.html', {'items': items})

@csrf_exempt
def profile_api(request):
    p, _ = Profile.objects.get_or_create(id=1)
    if request.method == 'GET':
        return JsonResponse({'name': p.name, 'skin_tone': p.skin_tone, 'skin_type': p.skin_type, 'body_type': p.body_type, 'gender': p.gender, 'location': p.location})
    if request.method == 'POST':
        data = json.loads(request.body)
        p.skin_tone = data.get('skin_tone')
        p.skin_type = data.get('skin_type')
        p.body_type = data.get('body_type')
        p.gender = data.get('gender')
        p.location = data.get('location')
        p.save()
        return JsonResponse({'status': 'saved'})

@csrf_exempt
def wardrobe_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item = WardrobeItem.objects.create(
            name=data.get('name'),
            color=data.get('color'),
            fabric=data.get('fabric'),
            occasion=data.get('occasion'),
            season=data.get('season'),
            category=data.get('category'),
        )
        return JsonResponse({'status': 'added', 'id': item.id})
    if request.method == 'GET':
        items = list(WardrobeItem.objects.values('id', 'name', 'color', 'fabric', 'occasion', 'season', 'category'))
        return JsonResponse({'items': items})
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
def wardrobe_delete_api(request, item_id):
    if request.method == 'DELETE':
        WardrobeItem.objects.filter(id=item_id).delete()
        return JsonResponse({'status': 'deleted'})
    return JsonResponse({'error': 'DELETE required'}, status=405)

@csrf_exempt
def recommend_outfits_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            from .ai_engine import recommend_from_wardrobe
            result = recommend_from_wardrobe(
                age=int(data.get('age', 25)),
                gender=data.get('gender', 'Female'),
                hydration=data.get('hydration', 'Medium'),
                oil=data.get('oil', 'Medium'),
                sensitivity=data.get('sensitivity', 'Low'),
                humidity=float(data.get('humidity', 50)),
                temperature=float(data.get('temperature', 25)),
                occasion=data.get('occasion', None),
                season=data.get('season', None),
                top_n=5
            )
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'POST required'}, status=405)

@csrf_exempt
def weather_api(request):
    location = request.GET.get('location', '').strip()
    if not location:
        return JsonResponse({'error': 'Location is required'}, status=400)
    api_key = settings.WEATHER_API_KEY
    base = 'https://api.openweathermap.org/data/2.5/weather'
    url = base + '?q=' + location + '&appid=' + api_key + '&units=metric'
    try:
        res = requests.get(url, timeout=5)
        data = res.json()
        if data.get('cod') != 200:
            return JsonResponse({'error': 'City not found'}, status=404)
        weather = {
            'location': data['name'] + ', ' + data['sys']['country'],
            'temperature': round(data['main']['temp']),
            'feels_like': round(data['main']['feels_like']),
            'condition': data['weather'][0]['main'],
            'description': data['weather'][0]['description'].title(),
            'humidity': data['main']['humidity'],
            'wind_speed': round(data['wind']['speed'] * 3.6, 1),
            'icon': data['weather'][0]['icon'],
        }
        p, _ = Profile.objects.get_or_create(id=1)
        from .models import WeatherLog
        WeatherLog.objects.create(
            profile=p,
            location=weather['location'],
            temperature=weather['temperature'],
            condition=weather['condition'],
            humidity=weather['humidity'],
            wind_speed=weather['wind_speed'],
        )
        return JsonResponse(weather)
    except requests.exceptions.Timeout:
        return JsonResponse({'error': 'Weather service timeout'}, status=503)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def save_outfit_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        p, _ = Profile.objects.get_or_create(id=1)
        from .models import OutfitHistory
        OutfitHistory.objects.create(
            profile=p,
            occasion=data.get('occasion', ''),
            profession=data.get('profession', ''),
            mood=data.get('mood', ''),
            colors_used=data.get('colors_used', ''),
            outfit_json=json.dumps(data.get('outfits', [])),
            location=data.get('location', ''),
            temperature=data.get('temperature'),
            condition=data.get('condition', ''),
        )
        return JsonResponse({'status': 'saved'})
    return JsonResponse({'error': 'POST required'}, status=405)

