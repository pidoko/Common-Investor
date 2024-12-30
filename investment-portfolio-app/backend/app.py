from flask import Flask, request, jsonify
import pandas as pd
import openai
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Set OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

from dotenv import load_dotenv

load_dotenv()

# Load the fixed CSV file on startup
CSV_FILE = "Curated_List_of_Companies_and_Securities.csv"
try:
    securities_df = pd.read_csv(CSV_FILE)
    securities_list = securities_df['Company or Security Name'].tolist()  # Adjust column name if necessary
except Exception as e:
    print(f"Error loading CSV file: {e}")
    securities_list = []

import logging
logging.basicConfig(level=logging.INFO)

@app.route('/generate-portfolio', methods=['POST'])
def generate_portfolio():
    data = request.json
    logging.info(f"Received data: {data}")
    risk = data.get('risk')
    time_frame = data.get('timeFrame')
    budget = data.get('budget')

    if not risk or not time_frame or not budget:
        return jsonify({'error': 'Invalid inputs'}), 400

    if not securities_list:
        return jsonify({'error': 'Securities list not loaded properly'}), 500

    # ChatGPT prompt
    prompt = f"""
As a seasoned Canadian portfolio manager who always provides some answer, Create a ${budget} investment portfolio for a {time_frame} holding period with a {risk} risk appetite, using the following securities: {', '.join(securities_list)}.
Show all the amounts to be invested on individual rows sorted from largest to smallest.
Discuss:
1. Portfolio allocations based on categorized asset classes.
2. The rationale behind the portfolio, including expected returns and risk optimization (using simplified Black-Litterman principles).
3. Budget optimization strategies and adjustments.
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an investment advisor."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500
        )
        portfolio = response['choices'][0]['message']['content'].strip()
        logging.info(f"Generated portfolio: {portfolio}")
        return jsonify({'portfolio': portfolio})
    except Exception as e:
        print(f"Error generating portfolio: {e}")
        return jsonify({'error': 'Failed to generate portfolio'}), 500

if __name__ == '__main__':
    app.run(debug=True)
