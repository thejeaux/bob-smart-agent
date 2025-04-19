from flask import Flask, request, render_template
from api_fetcher import fetch_user_bar
from analyzer import analyze_user_bar
from recommender import recommend_bottles
import pandas as pd

app = Flask(__name__)

# Load bottle dataset once
bottle_db = pd.read_csv('bottle_dataset.csv')

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        try:
            bar_data = fetch_user_bar(username)
            user_profile = analyze_user_bar(bar_data)
            recommendations = recommend_bottles(user_profile, bottle_db, top_n=5)
            diversify_recommendations = recommend_bottles(user_profile, bottle_db, top_n=3, diversify=True)
            return render_template('results.html', recs=recommendations, divers=diversify_recommendations)
        except Exception as e:
            return f"Error: {e}"
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)