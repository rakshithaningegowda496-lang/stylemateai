from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render

GENDER_CHOICES = ['Female', 'Male', 'Non-binary', 'Prefer Not To Say']

def profile_page(request):
    step = int(request.POST.get('step', request.GET.get('step', 1)))
    context = {
        'step': step,
        'name': request.POST.get('full_name', request.session.get('full_name', '')),
        'age': request.POST.get('age', request.session.get('age', '23')),
        'gender_identity': request.POST.get('gender_identity', request.session.get('gender_identity', 'Prefer Not To Say')),
        'skin_tone': request.POST.get('skin_tone', request.session.get('skin_tone', 'Fair')),
        'body_type': request.POST.get('body_type', request.session.get('body_type', 'Slim')),
        'skin_type': request.POST.get('skin_type', request.session.get('skin_type', 'Normal')),
        'gender': request.POST.get('gender', request.session.get('gender', 'Female')),
        'gender_choices': GENDER_CHOICES,
    }

    if request.method == 'POST':
        for key in ['full_name', 'age', 'gender_identity', 'skin_tone', 'body_type', 'skin_type', 'gender']:
            value = request.POST.get(key)
            if value is not None:
                request.session[key] = value

        if request.POST.get('action') == 'continue':
            context['step'] = 2
        elif request.POST.get('action') == 'back':
            context['step'] = 1
        elif request.POST.get('action') == 'finish':
            context['step'] = 2
            context['saved'] = True

    return render(request, 'profile.html', context)


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
