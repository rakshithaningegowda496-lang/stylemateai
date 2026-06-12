import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'style.settings')

import django
django.setup()

import cv2
import mediapipe as mp
from core.models import UserProfile

profile = UserProfile.objects.last()
print("Profile image path:", profile.profile_image.path)

img = cv2.imread(profile.profile_image.path)
print("Image shape:", img.shape if img is not None else "Could not load!")

# Try pose detection
import urllib.request
model_path = "pose_landmarker.task"
if not os.path.exists(model_path):
    print("Downloading model...")
    urllib.request.urlretrieve(
        "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/latest/pose_landmarker_lite.task",
        model_path
    )

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.IMAGE
)

with PoseLandmarker.create_from_options(options) as landmarker:
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    )
    result = landmarker.detect(mp_image)

print("Pose landmarks found:", len(result.pose_landmarks))
if result.pose_landmarks:
    lm = result.pose_landmarks[0]
    print("Left shoulder:", lm[11].x, lm[11].y)
    print("Right shoulder:", lm[12].x, lm[12].y)
else:
    print("NO POSE DETECTED - image may be cropped or low quality")