import requests
from frontend_inputs_ppxl_api import *
from datetime import datetime
ppxl_api_key = "Your_API_key"
url_ppxl = "https://api.perplexity.ai/chat/completions"
#  give rescource links, related video links and related image links for each query along answwer
def AI_tutor():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    payload = {
        "model": "mistral-7b-instruct",
        "messages": [
            {
                "role": "system",
                "content": f"You are a Classroom bot for {subject} subject. Generate response, rescource links, related video links and related image links in wolfram alpha mode."
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
        "doubts_left": doubts_left,
        "timestamp": timestamp,
        "subject": subject,
        "question": user_question,
        "answer": data['choices'][-1]['message']['content']
    }
    print(ai_tutor_json)
    return ai_tutor_json

















# def AI_tutor():
#     url = "https://api.perplexity.ai/chat/completions"
#     payload = {
#         "model": "mistral-7b-instruct",
#         "messages": [
#             {
#                 "role": "system",
#                 "content": "You are a Classroom bot for physics subject. Be precise and concise."
#             },
#             {
#                 "role": "user",
#                 "content": "how many oceans are there in the world"
#             }
#         ]
#     }
#     headers = {
#         "accept": "application/json",
#         "content-type": "application/json",
#         "authorization": f"Bearer Your_API_key"
#     }
#     response = requests.post(url, json=payload, headers=headers)
#     data = response.json()
#     ai_tutor_json = {
#         "answer": data['choices'][-1]['message']['content']
#     }
#     print(ai_tutor_json)
#     return ai_tutor_json

AI_tutor()