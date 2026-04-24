from django.http import JsonResponse
from .models import Profile
import json

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
