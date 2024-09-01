from pdfquery import PDFQuery
from flask import Flask, request, jsonify
import os



app = Flask(__name__)


@app.route('/IG', methods=['POST'])
def Summary():

    user_query1 = request.args.get('user_query')

    uploaded_file = request.files['pdf_file']

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
    
    user_query4 = f"""Create a very detailed teacher\'s quiz of 15 questions for a topic that focuses on subject_name with a title, type: MCQ and true/false. If takes no more than 15 to complete. 
        Return a JSON with double quotes with the following properties: 
        topic, duration, subject_name, title, description, questions;
        The topic, subject_name, title and description will be based on the Provided comtent.
        questions will have the properties as follows:   
        questionName , option1,  option2, option3, option4, explanation, answer note answer will be the value of the correct option and "type" of question is must field. 
        Explanation will be string with a small explanation of the answer of the question. if question type is True/False give only two options option1 and option2 
        with value of True and False of option1 and option2  else questionName, option1,  option2, option3, option4,  answer, duration, description."""

    # Generate the file path where you want to save the PDF
    save_path = os.path.join('C:\\Users', uploaded_file.filename)

    # Save the uploaded PDF to the specified directory
    uploaded_file.save(save_path)

    # Instantiate the PDFQuery class
    pdf_chatbot = PDFQuery(openai_api_key="YOUR_OPENAI_API_KEY")

    pdf_chatbot.ingest(save_path)

    answer1 = pdf_chatbot.ask(user_query1)
    answer2 = pdf_chatbot.ask(user_query2)
    answer3 = pdf_chatbot.ask(user_query3)
    answer4 = pdf_chatbot.ask(user_query4)


    # Clear loaded documents and chatbot state
    pdf_chatbot.forget()

    return jsonify({"summary": answer1,
                    "glossary": answer2,
                    "FlashCards": answer3,
                    "Quiz": answer4})



# @app.route('/generate_quiz', methods=['POST'])
# def generate_quiz():
    

#     user_query = f"""Create a very detailed teacher\'s quiz of 15 questions for a topic that focuses on subject_name with a title, type: MCQ and true/false. If takes no more than 15 to complete. Return a JSON with double quotes with the following properties: 
#             topic, duration, subject_name, title, description, questions;
#             The topic, subject_name, title and description will be based on the Provided comtent.
#             questions will have the properties as follows:   
#             questionName , option1,  option2, option3, option4, explanation, answer note answer will be the value of the correct option and "type" of question is must field. Explanation will be string with a small explanation of the answer of the question. if question type is True/False give only two options option1 and option2 
#             with value of True and False of option1 and option2  else questionName, option1,  option2, option3, option4,  answer, duration, description."""
    
#     uploaded_file = request.files['pdf_file']

#     # Generate the file path where you want to save the PDF
#     save_path = os.path.join('C:\\Users', uploaded_file.filename)

#     # Save the uploaded PDF to the specified directory
#     uploaded_file.save(save_path)

#     pdf_chatbot = PDFQuery(openai_api_key="YOUR_OPENAI_API_KEY")

#     pdf_chatbot.ingest(save_path)

#     answer = pdf_chatbot.ask(user_query)
#     print(answer)

#     # Clear loaded documents and chatbot state
#     pdf_chatbot.forget()

#     # # Delete the downloaded file after processing
#     os.remove(save_path)
#     return jsonify({"result": answer})



# @app.route('/glossary', methods=['POST'])
# def Glossary():

#     user_query2 = """Please create a glossary of key terms for the provided content. The glossary should include definitions for each term, 
#                     and the terms should be directly related to the main topic of the content. Return a JSON with double quotes with the following properties:
#                     Word, Meaning,
#                     Word should only contain words from the provided text,
#                     Meaning will be string with an explanation of the word of the provided content"""
#     uploaded_file = request.files['pdf_file']

#     # Generate the file path where you want to save the PDF
#     save_path = os.path.join('C:\\Users', uploaded_file.filename)

#     # Save the uploaded PDF to the specified directory
#     uploaded_file.save(save_path)
    

#     pdf_chatbot = PDFQuery(openai_api_key="YOUR_OPENAI_API_KEY")

#     pdf_chatbot.ingest(save_path)

#     answer2 = pdf_chatbot.ask(user_query2)
#     print(answer2)

#     # Clear loaded documents and chatbot state
#     pdf_chatbot.forget()

#     # Delete the downloaded file after processing
#     os.remove(save_path)

#     return jsonify({"result": answer2, 
#                     "flashcard": answer3,
#                     "summary": answer1}),


# @app.route('/flashCards', methods=['POST'])
# def glossary():

#     user_query3 = """Please create a set of flash cards based on the provided content. Each flash card should include a question on one side, 
#         and the answer or response on the other side. The questions should be designed to test understanding of the key concepts in the content.
#         Return a JSON with double quotes with the following properties:
#         Question, Response,
#         Questions should only contain context from the provided content in an interactive way,
#         Response will be string with an explanation or answer of the Question from the provided content in an interactive way"""

#     uploaded_file = request.files['pdf_file']

#     # Generate the file path where you want to save the PDF
#     save_path = os.path.join('C:\\Users', uploaded_file.filename)

#     # Save the uploaded PDF to the specified directory
#     uploaded_file.save(save_path)
    

#     pdf_chatbot = PDFQuery(openai_api_key="YOUR_OPENAI_API_KEY")

#     pdf_chatbot.ingest(save_path)

#     answer3 = pdf_chatbot.ask(user_query3)
#     print(answer3)

#     # Clear loaded documents and chatbot state
#     pdf_chatbot.forget()

#     # Delete the downloaded file after processing
#     os.remove(save_path)
#     return jsonify({"result": answer3})

    
if __name__ == '__main__':
    app.run(debug=True)
