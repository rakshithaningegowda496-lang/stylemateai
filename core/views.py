from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import UserProfile, WardrobeItem
import json
import requests
import base64
import anthropic



def home(request):
    return render(request, 'home.html')
GENDER_CHOICES = ['Female', 'Male', 'Non-binary', 'Prefer Not To Say']

def profile(request):
    # Always load existing profile
    try:
        p = UserProfile.objects.get(id=1)
    except UserProfile.DoesNotExist:
        p = None

    if request.method == 'POST':
        # Get or create profile id=1
        p, _ = UserProfile.objects.get_or_create(
            id=1,
            defaults={
                'full_name': '',
                'skin_tone': '',
                'body_type': '',
                'skin_type': '',
                'gender':    '',
            }
        )
        p.full_name = request.POST.get('full_name', '')
        p.age       = request.POST.get('age') or None
        p.skin_tone = request.POST.get('skin_tone', '')
        p.body_type = request.POST.get('body_type', '')
        p.skin_type = request.POST.get('skin_type', '')
        p.gender    = request.POST.get('gender', '')

        # ✅ Save whichever file input was used
        if 'profile_image' in request.FILES:
            p.profile_image = request.FILES['profile_image']
            print(f"DEBUG: Saving profile image: {request.FILES['profile_image'].name}")
        else:
            print("DEBUG: No profile_image in request.FILES")
            print(f"DEBUG: FILES keys = {list(request.FILES.keys())}")

        p.save()

        return render(request, 'profile.html', {
            'saved':     True,
            'profile':   p,
            'name':      p.full_name,
            'age':       p.age,
            'skin_tone': p.skin_tone,
            'body_type': p.body_type,
            'skin_type': p.skin_type,
            'gender':    p.gender,
        })

    # GET — load existing data into form
    context = {}
    if p:
        context = {
            'profile':   p,
            'name':      p.full_name,
            'age':       p.age,
            'skin_tone': p.skin_tone,
            'body_type': p.body_type,
            'skin_type': p.skin_type,
            'gender':    p.gender,
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
@csrf_exempt
def profile_api(request):
    p = get_profile()
    if request.method == 'GET':
        return JsonResponse({
            'name':              p.full_name,
            'skin_tone':         p.skin_tone,
            'skin_type':         p.skin_type,
            'body_type':         p.body_type,
            'gender':            p.gender,
            # ✅ THIS is what the styling page checks:
            'has_profile_image': bool(p.profile_image),
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

    if request.method == "POST":

        UserProfile.objects.create(
            full_name=request.POST.get('full_name'),
            age=request.POST.get('age'),
            skin_tone=request.POST.get('skin_tone'),
            body_type=request.POST.get('body_type'),
            skin_type=request.POST.get('skin_type'),
            gender=request.POST.get('gender'),
        )

        return render(request, 'profile.html', {
            'saved': True
        })

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
# ADD at the top with other imports:


# ADD this new view function:
@csrf_exempt
def generate_tryon_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        data        = json.loads(request.body)
        outfit_name = data.get('outfit_name', 'Selected Outfit')
        outfit_desc = data.get('outfit_description', '')
        outfit_pieces = data.get('outfit_pieces', [])

        # 1. Get profile (hardcoded id=1 like rest of your app)
        try:
            p = UserProfile.objects.get(id=1)
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'Profile not found. Please set up your profile first.'}, status=404)

        # 2. Check profile image
        if not p.profile_image:
            return JsonResponse({
                'error': 'No profile photo found. Please upload your photo on the Profile page first.',
                'needs_photo': True
            }, status=400)

        # 3. Read profile image → base64
        with open(p.profile_image.path, 'rb') as f:
            image_bytes = f.read()

        profile_b64 = base64.b64encode(image_bytes).decode('utf-8')
        ext = os.path.splitext(p.profile_image.name)[1].lower()
        mime_type = 'image/png' if ext == '.png' else 'image/jpeg'

        # 4. Build outfit description string
        pieces_text = '\n'.join(f'  - {piece}' for piece in outfit_pieces)
        outfit_full = f"""
Outfit: {outfit_name}
Description: {outfit_desc}
Pieces:
{pieces_text}
        """.strip()

        # 5. Call Claude with profile photo + outfit description
        client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

        response = client.messages.create(
            model='claude-opus-4-5',
            max_tokens=1000,
            messages=[{
                'role': 'user',
                'content': [
                    {
                        'type': 'image',
                        'source': {
                            'type': 'base64',
                            'media_type': mime_type,
                            'data': profile_b64
                        }
                    },
                    {
                        'type': 'text',
                        'text': f"""You are a warm, encouraging professional fashion stylist.

The person in the photo wants a virtual try-on analysis for this outfit:

{outfit_full}

Please provide:
1. ✨ How this outfit would look on them specifically (refer to what you see — their features, skin tone, body type)
2. 🎨 How well the colors complement their complexion
3. 👟 Specific accessory, footwear, and hair suggestions
4. ⭐ Style rating out of 10 with a reason

Be specific to THIS person. Be warm and confidence-boosting!"""
                    }
                ]
            }]
        )

        result = response.content[0].text

        return JsonResponse({
            'status':  'success',
            'result':  result,
            'outfit':  outfit_name
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def upload_profile_image_api(request):
    if request.method == 'POST':
        if 'profile_image' not in request.FILES:
            return JsonResponse({'error': 'No image provided'}, status=400)
        try:
            p = UserProfile.objects.get(id=1)
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'Profile not found'}, status=404)
        p.profile_image = request.FILES['profile_image']
        p.save()
        return JsonResponse({'status': 'uploaded'})
    return JsonResponse({'error': 'POST required'}, status=405)
@csrf_exempt
def generate_outfit_suggestions(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    try:
        data       = json.loads(request.body)
        occasion   = data.get('occasion', 'casual')
        mood       = data.get('mood', 'relaxed')
        colors     = data.get('colors', 'neutral')
        prof_style = data.get('profStyle', 'versatile')
        skin_tone  = data.get('skinTone', 'medium')
        profession = data.get('profession', '')

        prompt = f"""You are a professional fashion stylist AI.
Generate exactly 3 outfit suggestions for:
- Occasion: {occasion}
- Profession: {profession} (style: {prof_style})
- Mood: {mood}
- Skin tone: {skin_tone}
- Preferred colors: {colors}

Respond ONLY with a JSON array, no markdown, no extra text:
[
  {{
    "name": "Outfit name",
    "description": "Short description mentioning colors and style",
    "pieces": ["piece 1", "piece 2", "piece 3"],
    "colors": ["color1", "color2"]
  }}
]"""

        client   = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        response = client.messages.create(
            model='claude-opus-4-5',
            max_tokens=1000,
            messages=[{'role': 'user', 'content': prompt}]
        )
        raw    = response.content[0].text
        clean  = raw.replace('```json', '').replace('```', '').strip()
        outfits = json.loads(clean)
        return JsonResponse({'outfits': outfits})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)