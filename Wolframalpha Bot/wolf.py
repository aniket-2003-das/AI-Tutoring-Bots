import wolframalpha
from dotenv import load_dotenv
import os
from wolf_frontend_inputs import *

load_dotenv()
query = "minimum of y = 3x + 5y in the third quadrant"
def wolf(query):
    api_key = os.getenv("api_key")
    client = wolframalpha.Client(api_key)
    # query = "what is photosynthesis?"
    res = client.query(query)
    answer = next(res.results).text
    print(query)
    print(answer)
    print(res)
    return answer,


wolf(query)



# from flask import Flask, jsonify, request
# import wolframalpha
# from dotenv import load_dotenv
# import os

# load_dotenv()

# app = Flask(__name__)

# @app.route('/query1', methods=['POST'])
# def get_wolfram_response():
#     try:
#         data = request.get_json()
#         query = data.get('query')

#         api_key = os.getenv("api_key")
#         client = wolframalpha.Client(api_key)

#         res = client.query(query)
#         answer = next(res.results).text

#         response = {
#             'query': query,
#             'answer': answer
#         }

#         return jsonify(response)

#     except Exception as e:
#         return jsonify({'error': str(e)})

# if __name__ == '__main__':
#     app.run(debug=True)
