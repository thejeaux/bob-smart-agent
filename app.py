import os
from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load CSV safely
csv_path = os.path.join(os.path.dirname(__file__), "bottle_data.csv")
bottle_data = pd.read_csv(csv_path)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    username = request.form['username']
    user_bottles = bottle_data.sample(3).to_dict(orient='records')
    return render_template('results.html', recommendations=user_bottles)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

