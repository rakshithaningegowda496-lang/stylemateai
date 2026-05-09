import random

def ai_suggestion(profile):
    outfits = {
        "Slim": ["Oversized Hoodie", "Slim Fit Jeans"],
        "Athletic": ["Muscle Fit T-shirt", "Joggers"],
        "Pear": ["A-line Dress", "Wide Pants"],
        "Apple": ["V-neck Top", "Straight Jeans"],
        "Rectangle": ["Layered Outfit", "Jacket + Jeans"]
    }

    return random.choice(outfits.get(profile.body_type, ["Casual Wear"]))
