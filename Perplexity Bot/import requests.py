import requests
import json

url = "https://api.perplexity.ai/chat/completions"
payload = {
    "model": "codellama-34b-instruct",
    "messages": [
        {
            "role": "system",
            "content": """Wolfram|Alpha: How many oceans are there in the world
            Response: {response}
            Resource Links: {resource_links}
            Related Video Links: {related_video_links}
            Related Image Links: {related_image_links}"""
        },
        {
            "role": "user",
            "content": "What is the industry of company sherlocks-team.com?"
        }
    ],
    'temperature': 1
}
headers = {
    "Authorization": f"Bearer pplx-Your_API_key",  
    "accept": "application/json",
    "content-type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
# print(response)
print(json.dumps(response.json(), indent=2))