import os
import logging
from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    csv_path = os.path.join(os.path.dirname(__file__), "bottle_data.csv")
    bottle_data = pd.read_csv(csv_path)
    logger.info("CSV loaded successfully")
except Exception as e:
    logger.error(f"Failed to load CSV: {e}")
    bottle_data = pd.DataFrame()  # Prevent crash

@app.route('/')
def home():
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error rendering home: {e}")
        return "Error loading home page", 500

@app.route('/results', methods=['POST'])
def results():
    try:
        username = request.form['username']
        user_bottles = bottle_data.sample(3).to_dict(orient='records')
        return render_template('results.html', recommendations=user_bottles)
    except Exception as e:
        logger.error(f"Error generating results: {e}")
        return "Error generating results", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
