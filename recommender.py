# recommender.py

import pandas as pd
import random

def recommend_bottles(user_profile, bottle_db):
    recommendations = []

    # Weight settings
    w_region = 0.3
    w_style = 0.3
    w_price = 0.2
    w_barrel = 0.2

    for idx, bottle in bottle_db.iterrows():
        score = 0.0

        # Match Region
        if str(bottle.get('Region', '')).lower() == str(user_profile.get('favorite_region', '')).lower():
            score += w_region

        # Match Style
        if str(bottle.get('Style', '')).lower() == str(user_profile.get('favorite_style', '')).lower():
            score += w_style

        # Price Similarity
        target_price = user_profile.get('target_price', 0)
        bottle_price = bottle.get('Price', 0)
        if target_price and bottle_price:
            price_diff = abs(target_price - bottle_price)
            price_score = max(0, 1 - price_diff / target_price)
            score += price_score * w_price

        # Barrel Type Match (Optional)
        user_barrel = user_profile.get('favorite_barrel', '').lower()
        bottle_barrel = str(bottle.get('Barrel Type', '')).lower()
        if user_barrel and bottle_barrel and user_barrel in bottle_barrel:
            score += w_barrel

        recommendations.append((bottle['Name'], bottle['Price'], score, bottle['Style'], bottle['Region'], bottle['Barrel Type']))

    # Sort by score
    recommendations.sort(key=lambda x: x[2], reverse=True)

    # Build smart reasoning explanations
    top_recommendations = []
    for rec in recommendations[:5]:
        name, price, score, style, region, barrel = rec
        reason = build_reason(user_profile, style, region, price, barrel)
        top_recommendations.append((name, price, reason))

    return top_recommendations

def build_reason(user_profile, style, region, price, barrel):
    reasons = []

    if style:
        reasons.append(f"you enjoy {style.lower()} style")
    if region:
        reasons.append(f"you prefer spirits from the {region} category")
    if barrel:
        reasons.append(f"you appreciate {barrel.lower()} aging techniques")
    if price:
        reasons.append(f"you typically shop around ${int(price)}")

    return "Because " + ", and ".join(random.sample(reasons, min(2, len(reasons)))) + "."

