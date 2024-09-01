# chatbot.py
from main import *
from webquery import *
from flask import Flask, request,jsonify
app = Flask(__name__)

@app.route("/url", methods=['POST'])
def main():
    openai_api_key = "Your_API_Key"
    web_query = WebQuery(openai_api_key=openai_api_key)


    # data = request.get_json()
    # url = data.get('url')
    url = "https://en.wikipedia.org/wiki/Russo-Ukrainian_War"


    user_query1 = "Give a complete summary about the provided content."

    # user_query2 = """Please create a glossary of key terms for the provided content. The glossary should include definitions for each term, 
    #                 and the terms should be directly related to the main topic of the content. Return a JSON with double quotes with the following properties:
    #                 Word, Meaning,
    #                 Word should only contain words from the provided text,
    #                 Meaning will be string with an explanation of the word of the provided content."""
    
    # user_query3 = """Please create a set of flash cards based on the provided content. Each flash card should include a question on one side, 
    #     and the answer or response on the other side. The questions should be designed to test understanding of the key concepts in the content.
    #     Return a JSON with double quotes with the following properties:
    #     Question, Response,
    #     Questions should only contain context from the provided content in an interactive way,
    #     Response will be string with an explanation or answer of the Question from the provided content in an interactive way."""
    
    # user_query4 = f"""Create a very detailed teacher\'s quiz of 5 questions for a topic that focuses on subject_name with a title, type: MCQ and true/false. If takes no more than 10 to complete. 
    #     Return a JSON with double quotes with the following properties: 
    #     topic, duration, subject_name, title, description, questions;
    #     The topic, subject_name, title and description will be based on the Provided comtent.
    #     questions will have the properties as follows:   
    #     questionName , option1,  option2, option3, option4, explanation, answer note answer will be the value of the correct option and "type" of question is must field. 
    #     Explanation will be string with a small explanation of the answer of the question. if question type is True/False give only two options option1 and option2 
    #     with value of True and False of option1 and option2  else questionName, option1,  option2, option3, option4,  answer, duration, description."""


    web_query.ingest(url)



    answer1 = web_query.ask(user_query1)
    # answer2 = web_query.ask(user_query2)
    # answer3 = web_query.ask(user_query3)
    # answer4 = web_query.ask(user_query4)
    
    return jsonify({"summary": answer1})
                    # "glossary": answer2,
                    # "FlashCards": answer3,
                    # "Quiz": answer4})



if __name__ == "__main__":
    main()



