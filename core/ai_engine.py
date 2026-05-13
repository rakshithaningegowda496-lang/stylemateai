import pickle
import pandas as pd

# ── Load model & encoders ───────────────────────
model          = pickle.load(open("core/model.pkl",           "rb"))
le_gender      = pickle.load(open("core/le_gender.pkl",       "rb"))
le_hydration   = pickle.load(open("core/le_hydration.pkl",    "rb"))
le_oil         = pickle.load(open("core/le_oil.pkl",          "rb"))
le_sensitivity = pickle.load(open("core/le_sensitivity.pkl",  "rb"))
le_target      = pickle.load(open("core/label_encoder.pkl",   "rb"))

# ── Skin type → best colors ─────────────────────
SKIN_COLOR_MAP = {
    "Oily":        ["White", "Blue", "Grey", "Black"],
    "Dry":         ["Cream", "Peach", "Yellow", "Pink"],
    "Combination": ["Green", "Purple", "Navy", "Beige"],
    "Normal":      ["Red", "Orange", "Brown", "Teal"],
}

# ── Skin type → avoid fabrics ───────────────────
SKIN_FABRIC_MAP = {
    "Oily":        ["Silk", "Polyester"],
    "Dry":         ["Synthetic", "Nylon"],
    "Combination": ["Synthetic"],
    "Normal":      [],
}

def predict_skin_type(age, gender, hydration, oil, sensitivity, humidity, temperature):
    sample = pd.DataFrame([{
        "Age":             age,
        "Gender":          le_gender.transform([gender])[0],
        "Hydration_Level": le_hydration.transform([hydration])[0],
        "Oil_Level":       le_oil.transform([oil])[0],
        "Sensitivity":     le_sensitivity.transform([sensitivity])[0],
        "Humidity":        humidity,
        "Temperature":     temperature,
    }])
    pred = model.predict(sample)[0]
    return le_target.inverse_transform([pred])[0]


def recommend_from_wardrobe(age, gender, hydration, oil,
                             sensitivity, humidity, temperature,
                             occasion=None, season=None, top_n=5):
    """Recommend outfits from user's OWN wardrobe in DB"""

    # Step 1: Predict skin type
    skin_type     = predict_skin_type(age, gender, hydration, oil,
                                      sensitivity, humidity, temperature)
    good_colors   = SKIN_COLOR_MAP.get(skin_type, [])
    avoid_fabrics = SKIN_FABRIC_MAP.get(skin_type, [])

    # Step 2: Query user's wardrobe from DB
    from core.models import WardrobeItem
    qs = WardrobeItem.objects.all()

    if occasion:
        qs = qs.filter(occasion__icontains=occasion)
    if season:
        qs = qs.filter(season__icontains=season)
    if avoid_fabrics:
        for fabric in avoid_fabrics:
            qs = qs.exclude(fabric__icontains=fabric)

    # Step 3: Sort — color matches first
    all_items     = list(qs.values("id","name","color","fabric","occasion","season","category"))
    color_match   = [i for i in all_items if any(c.lower() in i["color"].lower() for c in good_colors)]
    others        = [i for i in all_items if i not in color_match]
    sorted_items  = (color_match + others)[:top_n]

    # Step 4: Fallback to CSV dataset if wardrobe is empty
    if not sorted_items:
        df = pd.read_csv("core/dataset/Wardrobe Assistant.csv")
        df = df[df["Gender"].str.lower() == gender.lower()]
        if occasion:
            df = df[df["occasion"].str.lower() == occasion.lower()]
        if avoid_fabrics:
            df = df[~df["fabric"].isin(avoid_fabrics)]
        color_match_df = df[df["color"].isin(good_colors)]
        others_df      = df[~df["color"].isin(good_colors)]
        df_sorted      = pd.concat([color_match_df, others_df]).head(top_n)
        sorted_items   = df_sorted[["product_name","color","occasion","season","fabric","categorize_outfit"]].to_dict(orient="records")
        source         = "dataset"
    else:
        source = "wardrobe"

    return {
        "skin_type":   skin_type,
        "good_colors": good_colors,
        "source":      source,   # "wardrobe" or "dataset"
        "outfits":     sorted_items
    }