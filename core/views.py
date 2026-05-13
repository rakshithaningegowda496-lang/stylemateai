from django.shortcuts import render
from django.http import JsonResponse


# HOME PAGE
def home(request):
    return render(request, 'home.html')


# PROFILE PAGE
def profile(request):
    return render(request, 'profile.html')


def profile_page(request):
    return render(request, 'profile.html')


# STYLING PAGE
def styling_page(request):
    return render(request, 'styling.html')


# TRY ON PAGE
def tryon(request):
    return render(request, 'tryon.html')


# FEEDBACK PAGE
def feedback(request):
    return render(request, 'feedback.html')


# WARDROBE PAGE
def wardrobe(request):
    return render(request, 'wardrobe.html')


# GENERATE OUTFIT API
def generate_outfit(request):

    data = {
        "status": "success",
        "message": "Outfit generated successfully"
    }

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