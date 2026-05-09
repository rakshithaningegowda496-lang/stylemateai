from django.shortcuts import render
from django.http import JsonResponse
from .models import UserProfile
from .utils import detect_skin_tone, detect_body_type


# Main Profile Page
def profile_page(request):
    return render(request, "profile.html")


# Save Profile + Analyze Image
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def save_profile(request):

    if request.method == "POST":

        name = request.POST.get("name")

        gender = request.POST.get("gender")

        age = request.POST.get("age")

        height = float(request.POST.get("height"))

        image = request.FILES.get("image")

        profile = UserProfile.objects.create(
            name=name,
            gender=gender,
            age=age,
            height=height,
            image=image
        )

        image_path = profile.image.path

        skin_tone = detect_skin_tone(image_path)

        body_type = detect_body_type(height)

        profile.skin_tone = skin_tone

        profile.body_type = body_type

        profile.save()

        return JsonResponse({
            "status":"success",
            "skin_tone":skin_tone,
            "body_type":body_type
        })

# Styling Page
def styling_page(request):
    return render(request, "styling.html")


# Try On Page
def tryon(request):
    return render(request, "tryon.html")


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
