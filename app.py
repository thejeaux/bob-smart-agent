from flask import Flask, render_template, request
import pandas as pd
import os
from recommender import recommend_bottles
from api_fetcher import fetch_user_data

app = Flask(__name__)

# Load the dataset once
bottle_db = pd.read_csv('bottle_data.csv')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    username = request.form['username']
    try:
        user_bottles = fetch_user_data(username)
        recommendations = recommend_bottles(user_bottles, bottle_db)
        return render_template('results.html', recommendations=recommendations)
    except Exception as e:
        return render_template('results.html', error=str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
