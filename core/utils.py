from PIL import Image
import numpy as np


def detect_skin_tone(image_path):

    image = Image.open(image_path).convert("RGB")

    image = image.resize((100, 100))

    pixels = np.array(image)

    avg_color = pixels.mean(axis=(0, 1))

    brightness = avg_color.mean()

    if brightness > 180:
        return "Fair"

    elif brightness > 120:
        return "Medium"

    else:
        return "Dark"


def detect_body_type(height):

    if height < 5:
        return "Slim"

    elif height < 5.8:
        return "Average"

    else:
        return "Athletic"