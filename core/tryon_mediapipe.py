import cv2
import numpy as np
import base64
import os
import sys
import tempfile
try:
    import mediapipe as mp  # type: ignore
except Exception as e:
    mp = None
    print(f"Warning: mediapipe import failed: {e}. Some functionality may be unavailable.", file=sys.stderr)

# rembg is optional; try to import at module load to avoid unresolved import warnings
try:
    from rembg import remove as rembg_remove  # type: ignore
except Exception:
    rembg_remove = None


def load_image(image_path):
    """Load image handling webp/avif formats."""
    import PIL.Image as PILImage
    ext = image_path.lower().split('.')[-1]

    if ext in ['webp', 'avif', 'heic']:
        try:
            pil_img = PILImage.open(image_path).convert('RGB')
            tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
            tmp.close()
            pil_img.save(tmp.name, 'PNG')
            img = cv2.imread(tmp.name)
            os.unlink(tmp.name)
            return img
        except Exception as e:
            print(f"Conversion failed: {e}", file=sys.stderr)
            return None

    return cv2.imread(image_path)


def load_image_rgba(image_path):
    """Load image as RGBA handling webp/avif formats."""
    import PIL.Image as PILImage
    ext = image_path.lower().split('.')[-1]

    if ext in ['webp', 'avif', 'heic']:
        try:
            pil_img = PILImage.open(image_path).convert('RGBA')
            tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
            tmp.close()
            pil_img.save(tmp.name, 'PNG')
            img = cv2.imread(tmp.name, cv2.IMREAD_UNCHANGED)
            os.unlink(tmp.name)
            return img
        except Exception as e:
            print(f"Conversion failed: {e}", file=sys.stderr)
            return None

    return cv2.imread(image_path, cv2.IMREAD_UNCHANGED)


def remove_background_rembg(img):
    """Remove garment background using rembg."""
    import PIL.Image as PILImage

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_img = PILImage.fromarray(img_rgb)

    if rembg_remove is not None:
        output = rembg_remove(pil_img)
        output_np = np.array(output)
        return cv2.cvtColor(output_np, cv2.COLOR_RGBA2BGRA)
    else:
        # Fallback simple background removal: treat near-white as background
        arr = np.array(pil_img)
        # create alpha mask where any channel is below threshold -> foreground
        thresh = 240
        mask = np.any(arr < thresh, axis=2).astype(np.uint8) * 255
        bgra = cv2.cvtColor(cv2.cvtColor(arr, cv2.COLOR_RGB2BGR), cv2.COLOR_BGR2BGRA)
        bgra[:, :, 3] = mask
        return bgra


def get_person_segmentation_mask(person_img):
    """Get person body segmentation mask using MediaPipe."""
    if mp is None:
        print("MediaPipe is not available. Please install mediapipe.", file=sys.stderr)
        return None

    model_path = os.path.join(os.path.dirname(__file__), "segmenter.tflite")

    if not os.path.exists(model_path):
        print("Segmentation model not found!", file=sys.stderr)
        return None

    BaseOptions = mp.tasks.BaseOptions
    ImageSegmenter = mp.tasks.vision.ImageSegmenter
    ImageSegmenterOptions = mp.tasks.vision.ImageSegmenterOptions
    VisionRunningMode = mp.tasks.vision.RunningMode

    options = ImageSegmenterOptions(
        base_options=BaseOptions(model_asset_path=model_path),
        running_mode=VisionRunningMode.IMAGE,
        output_category_mask=True,
    )

    with ImageSegmenter.create_from_options(options) as segmenter:
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=cv2.cvtColor(person_img, cv2.COLOR_BGR2RGB)
        )
        result = segmenter.segment(mp_image)

    category_mask = result.category_mask.numpy_view()
    print(f"Unique categories: {np.unique(category_mask)}", file=sys.stderr)

    person_mask = np.where(category_mask == 15, 255, 0).astype(np.uint8)

    if person_mask.max() == 0:
        print("Fallback: using all foreground", file=sys.stderr)
        person_mask = np.where(category_mask > 0, 255, 0).astype(np.uint8)

    return person_mask


def get_pose_landmarks(person_img):
    """Get body landmarks using MediaPipe Pose."""
    model_path = os.path.join(os.path.dirname(__file__), "pose_landmarker.task")

    if not os.path.exists(model_path):
        import urllib.request
        print("Downloading pose model...", file=sys.stderr)

        urllib.request.urlretrieve(
            "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/latest/pose_landmarker_lite.task",
            model_path
        )

    h, w = person_img.shape[:2]

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
            data=cv2.cvtColor(person_img, cv2.COLOR_BGR2RGB)
        )
        result = landmarker.detect(mp_image)

    if not result.pose_landmarks:
        return None

    lm = result.pose_landmarks[0]

    return {
        'ls': (int(lm[11].x * w), int(lm[11].y * h)),
        'rs': (int(lm[12].x * w), int(lm[12].y * h)),
        'lh': (int(lm[23].x * w), int(lm[23].y * h)),
        'rh': (int(lm[24].x * w), int(lm[24].y * h)),
    }


def apply_tryon(person_image_path, garment_image_path):

    person_img = load_image(person_image_path)
    if person_img is None:
        print("Failed to load person image!", file=sys.stderr)
        return None

    h, w = person_img.shape[:2]
    print(f"Person: {w}x{h}", file=sys.stderr)

    garment_img = load_image_rgba(garment_image_path)
    if garment_img is None:
        print("Failed to load garment image!", file=sys.stderr)
        return None

    print(f"Garment: {garment_img.shape}", file=sys.stderr)

    # Remove garment background
    print("Removing garment background...", file=sys.stderr)

    if garment_img.shape[2] == 3:
        garment_bgra = remove_background_rembg(garment_img)
    else:
        garment_bgra = remove_background_rembg(
            cv2.cvtColor(garment_img, cv2.COLOR_BGRA2BGR)
        )

    print("Garment background removed!", file=sys.stderr)

    # Pose detection
    print("Detecting pose...", file=sys.stderr)
    pose = get_pose_landmarks(person_img)

    if pose is None:
        print("No pose detected!", file=sys.stderr)
        return None

    ls, rs, lh, rh = pose['ls'], pose['rs'], pose['lh'], pose['rh']
    print(f"Pose → LS:{ls} RS:{rs} LH:{lh} RH:{rh}", file=sys.stderr)

    # Segmentation
    print("Segmenting person...", file=sys.stderr)
    seg_mask = get_person_segmentation_mask(person_img)

    # Garment placement
    shoulder_cx = (ls[0] + rs[0]) // 2
    shoulder_y = min(ls[1], rs[1])
    hip_y = max(lh[1], rh[1])

    body_height = hip_y - shoulder_y
    shoulder_w = abs(ls[0] - rs[0])

    garment_w = max(int(shoulder_w * 2.2), int(w * 0.60))
    garment_h = int(body_height * 1.20)

    x1 = max(0, shoulder_cx - garment_w // 2)
    y1 = max(0, shoulder_y - int(body_height * 0.05))
    x2 = min(w, x1 + garment_w)
    y2 = min(h, y1 + garment_h)

    garment_w = x2 - x1
    garment_h = y2 - y1

    print(f"Garment region: x1={x1} y1={y1} x2={x2} y2={y2}", file=sys.stderr)

    garment_resized = cv2.resize(
        garment_bgra,
        (garment_w, garment_h),
        interpolation=cv2.INTER_LANCZOS4
    )

    output = person_img.copy()

    garment_alpha = cv2.GaussianBlur(
        garment_resized[:, :, 3],
        (9, 9),
        0
    ).astype(float) / 255.0

    garment_rgb = garment_resized[:, :, :3].astype(float)
    body_region = output[y1:y2, x1:x2].astype(float)

    # FIXED SHAPE MISMATCH
    if seg_mask is not None:
        seg_region = seg_mask[y1:y2, x1:x2].astype(float) / 255.0

        if seg_region.shape != garment_alpha.shape:
            seg_region = cv2.resize(
                seg_region,
                (garment_alpha.shape[1], garment_alpha.shape[0])
            )

        seg_region = np.squeeze(seg_region)

        combined_alpha = garment_alpha * seg_region
    else:
        combined_alpha = garment_alpha

    combined_alpha_3ch = combined_alpha[:, :, np.newaxis]

    blended = (
        combined_alpha_3ch * garment_rgb
        + (1 - combined_alpha_3ch) * body_region
    )

    output[y1:y2, x1:x2] = np.clip(blended, 0, 255).astype(np.uint8)

    print("Done blending!", file=sys.stderr)

    _, buffer = cv2.imencode('.jpg', output)

    return f"data:image/jpeg;base64,{base64.b64encode(buffer).decode('utf-8')}"


if __name__ == "__main__":
    if len(sys.argv) == 3:
        person_path = sys.argv[1]
        garment_path = sys.argv[2]

        print(f"Person: {person_path}", file=sys.stderr)
        print(f"Garment: {garment_path}", file=sys.stderr)

        result = apply_tryon(person_path, garment_path)

        if result:
            print(result)
            print("SUCCESS!", file=sys.stderr)
        else:
            print("ERROR!", file=sys.stderr)
            sys.exit(1)