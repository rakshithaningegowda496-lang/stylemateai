import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import WardrobeItem 
from .models import UserProfile

# =========================
# PAGE VIEWS
# =========================

def home(request):
    return render(request, "home.html")



def profile(request):

    saved = False

    if request.method == 'POST':

        UserProfile.objects.create(
            full_name=request.POST.get('full_name'),
            age=request.POST.get('age'),
            skin_tone=request.POST.get('skin_tone'),
            body_type=request.POST.get('body_type'),
            skin_type=request.POST.get('skin_type'),
            gender=request.POST.get('gender'),
            profile_image=request.FILES.get('profile_image')
        )

    saved = True

    # ALWAYS FETCH PROFILE
    profile = UserProfile.objects.last()

    return render(request, 'profile.html', {
        'profile': profile,
        'saved': saved
    })


def wardrobe(request):
    items = WardrobeItem.objects.all().order_by('-id')

    return render(request, "wardrobe.html", {
        "items": items
    })
    
def styling_page(request):
    profile = UserProfile.objects.first()

    return render(request, "styling.html", {
        "profile": profile
    })


def tryon(request):
    return render(request, "tryon.html")


def feedback(request):
    return render(request, "feedback.html")


# =========================
# API VIEWS
# =========================

def profile_api(request):
    return JsonResponse({
        "success": True,
        "message": "Profile API working"
    })


def weather_api(request):
    return JsonResponse({
        "success": True,
        "weather": "Sunny"
    })


# =========================
# WARDROBE API
# =========================

@csrf_exempt
def wardrobe_api(request):

    if request.method == "GET":
        items = WardrobeItem.objects.all().order_by('-created_at')
        data = [
            {
                "id": item.id,
                "name": item.name,
                "category": item.category,
                "style_type": item.style_type,
                "color_name": item.color_name,
                "color_hex": item.color_hex,
                "image_url": item.image.url,
            }
            for item in items
        ]
        return JsonResponse({"success": True, "items": data})

    if request.method == "POST":
        try:
            name = request.POST.get("name")
            category = request.POST.get("category")
            style_type = request.POST.get("style_type")
            color_name = request.POST.get("color_name")
            color_hex = request.POST.get("color_hex", "#000000")
            image = request.FILES.get("image")

            if not all([name, category, style_type, color_name]):
                return JsonResponse({
                    "success": False,
                    "error": "Missing required fields: name, category, style_type, color_name"
                }, status=400)

            if not image:
                return JsonResponse({
                    "success": False,
                    "error": "No image uploaded"
                }, status=400)

            item = WardrobeItem.objects.create(
                name=name,
                category=category,
                style_type=style_type,
                color_name=color_name,
                color_hex=color_hex,
                image=image,
            )

            return JsonResponse({
                "success": True,
                "item": {
                    "id": item.id,
                    "name": item.name,
                    "category": item.category,
                    "style_type": item.style_type,
                    "color_name": item.color_name,
                    "color_hex": item.color_hex,
                    "image_url": item.image.url,
                }
            }, status=201)

        except Exception as e:
            return JsonResponse({
                "success": False,
                "error": str(e)
            }, status=500)

    return JsonResponse({"success": False, "error": "Method not allowed"}, status=405)


@csrf_exempt
@require_http_methods(["DELETE"])
def wardrobe_delete_api(request, item_id):
    try:
        item = WardrobeItem.objects.get(id=item_id)
        item.image.delete(save=False)  # also deletes file from disk
        item.delete()
        return JsonResponse({"success": True, "message": f"Item {item_id} deleted"})
    except WardrobeItem.DoesNotExist:
        return JsonResponse({"success": False, "error": "Item not found"}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


# =========================
# OUTFIT API
# =========================

@csrf_exempt
def save_outfit_api(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Method not allowed"}, status=405)
    try:
        body = json.loads(request.body)
        name = body.get("name", "")
        item_ids = body.get("item_ids", [])

        outfit = Outfit.objects.create(name=name)
        items = WardrobeItem.objects.filter(id__in=item_ids)
        outfit.items.set(items)
        outfit.save()

        return JsonResponse({
            "success": True,
            "outfit": {
                "id": outfit.id,
                "name": outfit.name,
                "item_ids": list(outfit.items.values_list('id', flat=True)),
            }
        }, status=201)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


def recommend_outfits_api(request):
    """
    Simple rule-based outfit recommendation.
    Extend this with AI/ML logic as needed.
    """
    try:
        style = request.GET.get("style", None)
        qs = WardrobeItem.objects.all()
        if style:
            qs = qs.filter(style_type=style)

        recommendations = {}
        for category in ['tops', 'bottoms', 'footwear', 'outerwear', 'accessories']:
            item = qs.filter(category=category).first()
            if item:
                recommendations[category] = {
                    "id": item.id,
                    "name": item.name,
                    "image_url": item.image.url,
                }

        return JsonResponse({"success": True, "recommendation": recommendations})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


def generate_outfit(request):
    """Page view for the outfit generator UI."""
    return render(request, "generate_outfit.html")


# =========================
# TRY-ON & PROFILE IMAGE
# =========================

@csrf_exempt
def generate_tryon_api(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Method not allowed"}, status=405)
    try:
        # Placeholder — integrate your try-on model/service here
        return JsonResponse({
            "success": True,
            "message": "Try-on generation triggered (stub)"
        })
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@csrf_exempt
def upload_profile_image_api(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Method not allowed"}, status=405)
    try:
        image = request.FILES.get("image")
        if not image:
            return JsonResponse({"success": False, "error": "No image provided"}, status=400)

        # Placeholder — save to profile model or session as needed
        return JsonResponse({
            "success": True,
            "message": "Profile image uploaded (stub)",
            "filename": image.name,
        })
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@csrf_exempt
def generate_outfit_suggestions(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Method not allowed"}, status=405)
    try:
        body = json.loads(request.body)
        style = body.get("style", "casual")
        occasion = body.get("occasion", "")

        # Placeholder — replace with AI suggestion logic
        return JsonResponse({
            "success": True,
            "suggestions": [],
            "message": f"Outfit suggestions for style='{style}', occasion='{occasion}' (stub)"
        })
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)