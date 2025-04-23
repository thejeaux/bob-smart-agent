import os
import pandas as pd
from flask import Flask, render_template, request

print("Starting app...")

app = Flask(__name__)

try:
    csv_path = os.path.join(os.path.dirname(__file__), "bottle_data.csv")
    print(f"Loading CSV from: {csv_path}")
    bottle_data = pd.read_csv(csv_path)
except Exception as e:
    print(f"Failed to load CSV: {e}")
    bottle_data = pd.DataFrame()  # fallback to empty DataFrame

@app.route('/')
def home():
    print("Serving home route")
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    username = request.form['username']
    print(f"Received request for username: {username}")
    user_bottles = bottle_data.sample(3).to_dict(orient='records')
    return render_template('results.html', recommendations=user_bottles)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"App running on port {port}")
    app.run(host='0.0.0.0', port=port)
