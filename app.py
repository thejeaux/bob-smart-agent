from flask import Flask, render_template, request
import pandas as pd
from recommender import recommend_bottles
from api_fetcher import fetch_user_data

app = Flask(__name__)

# Load the bottle database
bottle_db = pd.read_csv('bottle_dataset.csv')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    username = request.form['username']

    try:
        user_bottles = fetch_user_data(username)
    except Exception as e:
        print(f"[ERROR] {e}")
        return render_template('results.html', recommendations=[], error=str(e))

    if not user_bottles:
        return render_template('results.html', recommendations=[], error="No bottles found for this user.")

    # Build a user profile based on available real data
    first_bottle = user_bottles[0]['product']

    preferred_region = first_bottle.get('spirit', 'Whiskey')
    preferred_style = "Rich"
    target_price = user_bottles[0].get('price', 50)
    preferred_barrel = "New Oak"

    user_profile = {
        'favorite_region': preferred_region,
        'favorite_style': preferred_style,
        'target_price': target_price,
        'favorite_barrel': preferred_barrel
    }

    recommendations = recommend_bottles(user_profile, bottle_db)

    return render_template('results.html', recommendations=recommendations, error=None)

if __name__ == "__main__":
    app.run(debug=True)
