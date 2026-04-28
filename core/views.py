from django.http import HttpResponse, JsonResponse
from .models import Profile
from django.shortcuts import render
from .models import UserProfile
import json
from django.views.decorators.csrf import csrf_exempt
from .ml_model import predict_outfit


# 🔹 PROFILE API
def profile_api(request):
    profile, created = Profile.objects.get_or_create(id=1)

    if request.method == "GET":
        return JsonResponse({
            "name": profile.name,
            "skin_tone": profile.skin_tone,
            "skin_type": profile.skin_type,
            "body_type": profile.body_type,
            "gender": profile.gender,
            "location": profile.location
        })

    if request.method == "POST":
        data = json.loads(request.body)

        profile.skin_tone = data.get("skin_tone")
        profile.skin_type = data.get("skin_type")
        profile.body_type = data.get("body_type")
        profile.gender = data.get("gender")
        profile.location = data.get("location")

        profile.save()

        return JsonResponse({"status": "saved"})

<<<<<<< HEAD
def styling(request):
    # your logic
    return HttpResponse("Styling page")

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
=======

# 🔹 GENERATE OUTFIT (AI)
@csrf_exempt
def generate_outfit(request):
    if request.method == "POST":
        data = json.loads(request.body)

        occasion = data.get("occasion")
        mood = data.get("mood")

        outfit = predict_outfit(occasion, mood)

        return JsonResponse({"outfit": outfit})

    return JsonResponse({"error": "Only POST allowed"})
from django.shortcuts import render

def styling_page(request):
    return render(request, "styling.html")
>>>>>>> 02e436f84cf7aeb21df953b9fc65d8b533f4d188
