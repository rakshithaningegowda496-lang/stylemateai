from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Profile, UserProfile, WardrobeItem
import json
import requests


def home(request):
    return render(request, 'home.html')


def profile_page(request):
    step = 1
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "continue":
            step = 2
        elif action == "back":
            step = 1
    return render(request, 'profile.html', {"step": step})


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


def styling_page(request):
    return render(request, 'styling.html')


def tryon(request):
    return render(request, 'tryon.html')


def feedback(request):
    return render(request, 'feedback.html')


def wardrobe(request):
    items = WardrobeItem.objects.all()
    return render(request, 'wardrobe.html', {'items': items})


def generate_outfit(request):
    return JsonResponse({"status": "success", "outfit": "Casual Jeans + White Shirt"})


@csrf_exempt
def profile_api(request):
    p, _ = Profile.objects.get_or_create(id=1)
    if request.method == 'GET':
        return JsonResponse({
            'name': p.name,
            'skin_tone': p.skin_tone,
            'skin_type': p.skin_type,
            'body_type': p.body_type,
            'gender': p.gender,
            'location': p.location
        })
    if request.method == 'POST':
        data = json.loads(request.body)
        p.skin_tone = data.get('skin_tone')
        p.skin_type = data.get('skin_type')
        p.body_type = data.get('body_type')
        p.gender    = data.get('gender')
        p.location  = data.get('location')
        p.save()
        return JsonResponse({'status': 'saved'})


@csrf_exempt
def wardrobe_api(request):
    if request.method == 'POST':
        try:
            name       = request.POST.get('name', '').strip()
            category   = request.POST.get('category', '').strip()
            style_type = request.POST.get('style_type', '').strip()
            color_name = request.POST.get('color_name', '').strip()
            color_hex  = request.POST.get('color_hex', '#000000').strip()
            image_file = request.FILES.get('image')

            if not all([name, category, style_type, color_name, image_file]):
                return JsonResponse({'success': False, 'error': 'All fields are required.'}, status=400)

            item = WardrobeItem.objects.create(
                name       = name,
                category   = category,
                style_type = style_type,
                color_name = color_name,
                color_hex  = color_hex,
                image      = image_file,
            )

            return JsonResponse({
                'success': True,
                'item': {
                    'id':         item.id,
                    'name':       item.name,
                    'category':   item.category,
                    'style_type': item.style_type,
                    'color_name': item.color_name,
                    'color_hex':  item.color_hex,
                    'image_url':  item.image.url,
                }
            }, status=201)

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    if request.method == 'GET':
        items = list(WardrobeItem.objects.values(
            'id', 'name', 'category', 'style_type', 'color_name', 'color_hex'
        ))
        return JsonResponse({'items': items})

    return JsonResponse({'error': 'Invalid method'}, status=405)


@csrf_exempt
def wardrobe_delete_api(request, item_id):
    if request.method == 'DELETE':
        try:
            item = WardrobeItem.objects.get(id=item_id)
            if item.image:
                import os
                if os.path.isfile(item.image.path):
                    os.remove(item.image.path)
            item.delete()
            return JsonResponse({'success': True})
        except WardrobeItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found.'}, status=404)
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
    url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric'
    try:
        res  = requests.get(url, timeout=5)
        data = res.json()
        if data.get('cod') != 200:
            return JsonResponse({'error': 'City not found'}, status=404)
        weather = {
            'location':    data['name'] + ', ' + data['sys']['country'],
            'temperature': round(data['main']['temp']),
            'feels_like':  round(data['main']['feels_like']),
            'condition':   data['weather'][0]['main'],
            'description': data['weather'][0]['description'].title(),
            'humidity':    data['main']['humidity'],
            'wind_speed':  round(data['wind']['speed'] * 3.6, 1),
            'icon':        data['weather'][0]['icon'],
        }
        p, _ = Profile.objects.get_or_create(id=1)
        from .models import WeatherLog
        WeatherLog.objects.create(
            profile=p, location=weather['location'],
            temperature=weather['temperature'], condition=weather['condition'],
            humidity=weather['humidity'], wind_speed=weather['wind_speed'],
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