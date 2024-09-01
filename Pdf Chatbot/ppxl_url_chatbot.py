from flask import Flask, jsonify, request
import requests

app = Flask(__name__)


added_text = """In the last chapter we developed the concepts of position,
    displacement, velocity and acceleration that are needed to
    describe the motion of an object along a straight line. We
    found that the directional aspect of these quantities can be
    taken care of by + and – signs, as in one dimension only two
    directions are possible. But in order to describe motion of an
    object  in  two  dimensions  (a  plane)  or  three  dimensions
    (space),  we  need  to  use  vectors  to  describe  the  above-
    mentioned physical quantities.  Therefore, it is first necessary
    to learn the language of vectors. What is a vector? How to
    add, subtract and multiply vectors ? What is the result of
    multiplying a vector by a real number ? We shall learn this
    to  enable  us  to  use  vectors  for  defining  velocity  and
    acceleration in a plane. We then discuss motion of an object
    in a plane.  As a simple case of motion in a plane, we shall
    discuss motion with constant acceleration and treat in detail
    the projectile motion. Circular motion is a familiar class of
    motion that has a special significance in daily-life situations.
    We shall discuss uniform circular motion in some detail.
    The equations developed in this chapter for motion in a
    plane can be easily extended to the case of three dimensions."""


user_query1 = "Give a complete summary about the provided content."

user_query2 = """Please create a glossary of key terms for the provided content. The glossary should include definitions for each term, 
                and the terms should be directly related to the main topic of the content. Return a JSON with double quotes with the following properties:
                Word, Meaning,
                Word should only contain words from the provided text,
                Meaning will be string with an explanation of the word of the provided content."""

user_query3 = """Please create a set of flash cards based on the provided content. Each flash card should include a question on one side, 
    and the answer or response on the other side. The questions should be designed to test understanding of the key concepts in the content.
    Return a JSON with double quotes with the following properties:
    Question, Response,
    Questions should only contain context from the provided content in an interactive way,
    Response will be string with an explanation or answer of the Question from the provided content in an interactive way."""

user_query4 = f"""Create a very detailed teacher\'s quiz of 5 questions for a topic that focuses on subject_name with a title, type: MCQ and true/false. If takes no more than 10 to complete. 
    Return a JSON with double quotes with the following properties: 
    topic, duration, subject_name, title, description, questions;
    The topic, subject_name, title and description will be based on the Provided comtent.
    questions will have the properties as follows:   
    questionName , option1,  option2, option3, option4, explanation, answer note answer will be the value of the correct option and "type" of question is must field. 
    Explanation will be string with a small explanation of the answer of the question. if question type is True/False give only two options option1 and option2 
    with value of True and False of option1 and option2  else questionName, option1,  option2, option3, option4,  answer, duration, description."""


@app.route('/summary', methods=['POST'])
def summary():
    url = "https://api.perplexity.ai/chat/completions"

    payload = {
        "model": "mistral-7b-instruct",
        "messages": [
            {
                "role": "system",
                "content": "Be precise and concise."
            },
            {
                "role": "user",
                "content": added_text+ f"for the above text {user_query1}"
            }
        ]
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer pplx-token"
    }

    response = requests.post(url, json=payload, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract and print the result
        result = response.json()["choices"][0]["message"]["content"]
        print(result)
        return jsonify({"summary": result})


@app.route('/glossary', methods=['POST'])
def glossary():
    url = "https://api.perplexity.ai/chat/completions"

    payload = {
        "model": "mistral-7b-instruct",
        "messages": [
            {
                "role": "system",
                "content": "Be precise and concise."
            },
            {
                "role": "user",
                "content": added_text+ f"for the above text {user_query2}"
            }
        ]
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer pplx-token"
    }

    response = requests.post(url, json=payload, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract and print the result
        result = response.json()["choices"][0]["message"]["content"]
        print(result)
        return jsonify({"glossary": result})





@app.route('/flashCards', methods=['POST'])
def flash_cards():
    url = "https://api.perplexity.ai/chat/completions"

    payload = {
        "model": "mistral-7b-instruct",
        "messages": [
            {
                "role": "system",
                "content": "Be precise and concise."
            },
            {
                "role": "user",
                "content": added_text+ f"for the above text {user_query3}"
            }
        ]
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer pplx-token"
    }

    response = requests.post(url, json=payload, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract and print the result
        result = response.json()["choices"][0]["message"]["content"]
        print(result)
        return jsonify({"flashcards": result})





@app.route('/Quiz', methods=['POST'])
def Quiz():
    url = "https://api.perplexity.ai/chat/completions"

    payload = {
        "model": "mistral-7b-instruct",
        "messages": [
            {
                "role": "system",
                "content": "Be precise and concise."
            },
            {
                "role": "user",
                "content": added_text+ f"for the above text {user_query4}"
            }
        ]
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer pplx-Token"
    }

    response = requests.post(url, json=payload, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract and print the result
        result = response.json()["choices"][0]["message"]["content"]
        print(result)
        return jsonify({"quiz": result})



if __name__ == '__main__':
    app.run(debug=True)



