import pandas as pd

def recommend_bottles(user_profile, bottle_db, top_n=5, diversify=False):
    recommendations = []

    for idx, bottle in bottle_db.iterrows():
        score = 0

        if 'region' in bottle and bottle['region'] in user_profile.get('favorite_regions', {}):
            score += user_profile['favorite_regions'][bottle['region']] * 2

        if 'style' in bottle and bottle['style'] in user_profile.get('favorite_styles', {}):
            score += user_profile['favorite_styles'][bottle['style']] * 3

        if 'price' in bottle and user_profile.get('avg_price'):
            price_diff = abs(bottle['price'] - user_profile['avg_price'])
            score += max(0, 50 - price_diff)

        if 'age' in bottle and user_profile.get('avg_age') and pd.notna(bottle['age']):
            age_diff = abs(bottle['age'] - user_profile['avg_age'])
            score += max(0, 20 - age_diff)

        recommendations.append((bottle['name'], score, bottle))

    recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)

    if diversify:
        favorite_regions = user_profile.get('favorite_regions', {})
        favorite_styles = user_profile.get('favorite_styles', {})

        top_region = max(favorite_regions, key=favorite_regions.get) if favorite_regions else None
        top_style = max(favorite_styles, key=favorite_styles.get) if favorite_styles else None

        diverse_recommendations = []
        for name, score, bottle in recommendations:
            if bottle['region'] != top_region and bottle['style'] != top_style:
                diverse_recommendations.append({
                    'name': name,
                    'price': bottle['price'],
                    'region': bottle['region'],
                    'age': bottle.get('age', 'N/A'),
                    'style': bottle['style'],
                    'reason': f"Suggested to diversify your bar — a {bottle['style']} whisky from {bottle['region']}."
                })
            if len(diverse_recommendations) >= top_n:
                break
        return diverse_recommendations

    final_recommendations = []
    for name, score, bottle in recommendations[:top_n]:
        explanation = f"Recommended because it matches your preference for {bottle['region']} and {bottle['style']} style, and is close to your price (${bottle['price']})."
        final_recommendations.append({
            'name': name,
            'price': bottle['price'],
            'region': bottle['region'],
            'age': bottle.get('age', 'N/A'),
            'style': bottle['style'],
            'reason': explanation
        })

    return final_recommendations