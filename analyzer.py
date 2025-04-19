import pandas as pd

# Style guessing function
def guess_style(bottle_name):
    name = bottle_name.lower()
    if any(word in name for word in ['ardbeg', 'lagavulin', 'laphroaig', 'caol ila', 'bowmore']):
        return 'Peated'
    if any(word in name for word in ['macallan', 'sherry', 'aberlour', 'glenfarclas']):
        return 'Sherried'
    if any(word in name for word in ['glenfiddich', 'yamazaki', 'hibiki', 'balvenie']):
        return 'Fruity'
    if any(word in name for word in ['redbreast', 'irish', 'midleton']):
        return 'Rich'
    return 'Unknown'

def analyze_user_bar(bar_data):
    df = pd.DataFrame(bar_data)

    # Only guess styles if 'name' column exists
    if 'name' in df.columns:
        if 'style' not in df.columns or df['style'].isnull().all():
            df['style'] = df['name'].apply(guess_style)

    analysis = {}

    if 'region' in df.columns:
        top_regions = df['region'].value_counts().head(3).to_dict()
        analysis['favorite_regions'] = top_regions

    if 'style' in df.columns:
        top_styles = df['style'].value_counts().head(3).to_dict()
        analysis['favorite_styles'] = top_styles

    if 'price' in df.columns:
        avg_price = df['price'].mean()
        analysis['avg_price'] = avg_price

    if 'age' in df.columns:
        df['age'] = pd.to_numeric(df['age'], errors='coerce')
        avg_age = df['age'].dropna().mean()
        analysis['avg_age'] = avg_age

    return analysis