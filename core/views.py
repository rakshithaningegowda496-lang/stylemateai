import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import WardrobeItem 
from .models import UserProfile
from django.conf import settings
from groq import Groq
import os
import requests

# When creating the client in your views, use:

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
    profile = UserProfile.objects.last()
    if not profile:
        return JsonResponse({"success": False, "error": "No profile found"}, status=404)
    return JsonResponse({
        "success": True,
        "skin_tone": profile.skin_tone,
        "body_type": profile.body_type,
        "gender": profile.gender,
        "full_name": profile.full_name,
        "has_profile_image": bool(profile.profile_image),
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
        return JsonResponse({"error": "Method not allowed"}, status=405)
    try:
        body = json.loads(request.body)
        outfit_name        = body.get("outfit_name", "")
        outfit_description = body.get("outfit_description", "")
        outfit_pieces      = body.get("outfit_pieces", [])

        profile = UserProfile.objects.last()
        if not profile or not profile.profile_image:
            return JsonResponse({"status": "error", "needs_photo": True})

        prompt = f"""You are a fashion stylist. Analyse how this outfit would look on the user.

Outfit: {outfit_name}
Description: {outfit_description}
Pieces: {', '.join(outfit_pieces)}

User profile:
- Skin tone: {profile.skin_tone}
- Body type: {profile.body_type}
- Gender: {profile.gender}"""

        client = Groq(api_key=settings.GROQ_API_KEY)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600,
        )
        return JsonResponse({
            "status": "success",
            "result": response.choices[0].message.content,
            "outfit": outfit_name,
        })

    except Exception as e:
        return JsonResponse({"status": "error", "error": str(e)}, status=500)

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
        return JsonResponse({"error": "Method not allowed"}, status=405)
    try:
        body = json.loads(request.body)
        occasion   = body.get("occasion", "casual")
        mood       = body.get("mood", "relaxed")
        colors     = body.get("colors", "neutral tones")
        profession = body.get("profession", "")
        prof_style = body.get("profStyle", "versatile")

        profile   = UserProfile.objects.last()
        skin_tone = profile.skin_tone if profile else "medium"

        wardrobe_items = WardrobeItem.objects.all()
        wardrobe_text = "\n".join([
            f"- {item.name} ({item.category}, {item.color_name}, {item.style_type})"
            for item in wardrobe_items
        ]) or "No wardrobe items yet."

        prompt = f"""You are a fashion stylist. Return ONLY a JSON object, no other text.

{{
  "outfits": [
    {{
      "name": "Outfit name here",
      "description": "Brief description here",
      "pieces": ["piece 1", "piece 2", "piece 3"],
      "colors": ["Color1", "Color2"]
    }},
    {{
      "name": "Outfit name here",
      "description": "Brief description here",
      "pieces": ["piece 1", "piece 2", "piece 3"],
      "colors": ["Color1", "Color2"]
    }},
    {{
      "name": "Outfit name here",
      "description": "Brief description here",
      "pieces": ["piece 1", "piece 2", "piece 3"],
      "colors": ["Color1", "Color2"]
    }}
  ]
}}

Suggest 3 outfits for:
- Skin tone: {skin_tone}
- Profession: {profession}
- Occasion: {occasion}
- Mood: {mood}
- Colors: {colors}
- Wardrobe items: {wardrobe_text}

Remember: Return ONLY the JSON, nothing else."""

        client = Groq(api_key=settings.GROQ_API_KEY)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
        )

        raw = response.choices[0].message.content.strip()
        print("GROQ RAW RESPONSE:", raw)

        # Remove markdown code blocks if model adds them
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()

        data = json.loads(raw)

        # ✅ Match each outfit's pieces to real wardrobe images
        wardrobe_list = list(WardrobeItem.objects.exclude(image='').values(
            'name', 'category', 'color_name', 'image'
        ))

        print("WARDROBE LIST:", wardrobe_list)  # debug

        for outfit in data.get("outfits", []):
            outfit["item_images"] = []
            for piece in outfit.get("pieces", []):
                piece_lower = piece.lower()
                best_match = None
                for item in wardrobe_list:
                    item_name     = item["name"].lower()
                    item_category = item["category"].lower()
                    # Match if any word in item name appears in piece or vice versa
                    if (item_name in piece_lower or
                        piece_lower in item_name or
                        item_category in piece_lower or
                        any(word in piece_lower for word in item_name.split())):
                        best_match = item
                        break
                if best_match:
                    image_url = settings.MEDIA_URL + best_match["image"]
                    outfit["item_images"].append(image_url)
                    print(f"  ✅ Matched '{piece}' → {best_match['name']} → {image_url}")
                else:
                    print(f"  ❌ No match for piece: '{piece}'")

        return JsonResponse(data)

    except json.JSONDecodeError as e:
        return JsonResponse({"error": f"JSON parse error: {str(e)}"}, status=500)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def generate_tryon_ai(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    try:
        body = json.loads(request.body)
        outfit_image_url = body.get("outfit_image_url", "")

        profile = UserProfile.objects.last()
        if not profile or not profile.profile_image:
            return JsonResponse({"status": "error", "needs_photo": True})

        person_path  = profile.profile_image.path
        garment_path = os.path.join(
            settings.MEDIA_ROOT,
            outfit_image_url.lstrip("/").replace("media/", "", 1)
        )

        print("👤 Person:", person_path)
        print("👗 Garment:", garment_path)

        # Run mediapipe using Python 3.11
        import subprocess, json as json_lib
        py311 = r"C:\Users\hp\AppData\Local\Programs\Python\Python311\python.exe"
        script = os.path.join(settings.BASE_DIR, "core", "tryon_mediapipe.py")

        result = subprocess.run(
            [py311, script, person_path, garment_path],
            capture_output=True,
            text=True,
            timeout=180
        )

        print("STDOUT:", result.stdout[:500])
        print("STDERR:", result.stderr[:1000])

        if result.returncode == 0 and result.stdout.strip():
            return JsonResponse({
                "status": "success",
                "tryon_image_url": result.stdout.strip(),
            })
        else:
            return JsonResponse({
                "status": "error",
                "error": "Pose detection failed. Use a clear full-body photo."
            }, status=500)

    except Exception as e:
        print("❌ Error:", str(e))
        return JsonResponse({"status": "error", "error": str(e)}, status=500)