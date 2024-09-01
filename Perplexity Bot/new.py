from flask import Flask, request
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import torch
from transformers import pipeline

# Load environment variables from .env file
load_dotenv()

# Access environment variables
ppxl_api_key = os.getenv("ppxl_api_key")
url_ppxl = os.getenv("url_ppxl")

app = Flask(__name__)

# Load sentiment analysis model from transformers library
sentiment_analyzer = pipeline('sentiment-analysis')

@app.route("/school/recommend1", methods=['POST'])
def AI_tutor():
    data = request.get_json()
    doubts_left = data.get('doubts_left')
    subject = data.get('subject')
    user_question = data.get('user_question')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Perform sentiment analysis using PyTorch model
    sentiment_result = sentiment_analyzer(user_question)

    payload = {
        "model": "mistral-7b-instruct",
        "messages": [
            {
                "role": "system",
                "content": f"You are a Classroom bot for {subject} subject. Be precise and concise."
            },
            {
                "role": "user",
                "content": f"{user_question}"
            }
        ]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {ppxl_api_key}"
    }
    response = requests.post(url_ppxl, json=payload, headers=headers)
    data = response.json()
    ai_tutor_json = {
        "answer": data['choices'][-1]['message']['content'],
        "doubts_left": doubts_left,
        "timestamp": timestamp,
        "subject": subject,
        "question": user_question,
        "sentiment": sentiment_result[0]['label']
    }
    print(ai_tutor_json)
    return ai_tutor_json

if __name__ == '__main__':
    app.run()
