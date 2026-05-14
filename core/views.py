from django.shortcuts import render
from django.http import JsonResponse
<<<<<<< HEAD
=======
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Profile, UserProfile, WardrobeItem
import json
import requests
>>>>>>> e3f31d3a65a145681ecf7b69a486148cd49f9ca2


# HOME PAGE
def home(request):
    return render(request, 'home.html')
<<<<<<< HEAD


# PROFILE PAGE
def profile(request):
    return render(request, 'profile.html')

=======
GENDER_CHOICES = ['Female', 'Male', 'Non-binary', 'Prefer Not To Say']
>>>>>>> e3f31d3a65a145681ecf7b69a486148cd49f9ca2

def profile_page(request):
<<<<<<< HEAD
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
=======
    return render(request, 'profile.html')
>>>>>>> 6d37e1cc662eea23e875d3e7e8eba627b445d562


# STYLING PAGE
def styling_page(request):
<<<<<<< HEAD
=======
    return render(request, "styling.html")
>>>>>>> e3f31d3a65a145681ecf7b69a486148cd49f9ca2
    return render(request, 'styling.html')


# TRY ON PAGE
def tryon(request):
    return render(request, 'tryon.html')


# FEEDBACK PAGE
def feedback(request):
    return render(request, 'feedback.html')

<<<<<<< HEAD
=======
# Feedback Page
def feedback(request):
    return render(request, "feedback.html")
>>>>>>> e3f31d3a65a145681ecf7b69a486148cd49f9ca2

# WARDROBE PAGE
def wardrobe(request):
    return render(request, 'wardrobe.html')


# GENERATE OUTFIT API
def generate_outfit(request):

<<<<<<< HEAD
    data = {
        "status": "success",
        "message": "Outfit generated successfully"
    }
=======
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
>>>>>>> e3f31d3a65a145681ecf7b69a486148cd49f9ca2

    return JsonResponse(data)


# PROFILE API
def profile_api(request):

    data = {
        "name": "Pramod",
        "email": "pramod@example.com"
    }

    return JsonResponse(data)


# WEATHER API
def weather_api(request):

    data = {
        "temperature": "28°C",
        "condition": "Cloudy"
    }

    return JsonResponse(data)


# SAVE OUTFIT API
def save_outfit_api(request):
<<<<<<< HEAD

    data = {
        "status": "saved"
    }

    return JsonResponse(data)


# WARDROBE API
def wardrobe_api(request):

    data = {
        "items": []
    }

    return JsonResponse(data)


# DELETE WARDROBE ITEM API
def wardrobe_delete_api(request, item_id):

    data = {
        "deleted_item_id": item_id
    }

    return JsonResponse(data)


# RECOMMEND OUTFITS API
def recommend_outfits_api(request):

    data = {
        "recommendations": [
            "Casual Shirt + Jeans",
            "Formal Blazer + Pants"
        ]
    }

    return JsonResponse(data)
=======
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

>>>>>>> e3f31d3a65a145681ecf7b69a486148cd49f9ca2
