from agent import Agent

from flask import Flask, request, jsonify
from io import BytesIO
import base64
import os
app = Flask(__name__)


@app.route('/chatbot2', methods=['POST'])
def pdf_requester():
    user_query ="describe the pdf ?"
    uploaded_file = request.files['pdf_file']

    # Generate the file path where you want to save the PDF
    save_path = os.path.join('C:\\Users', uploaded_file.filename)

    # Save the uploaded PDF to the specified directory
    uploaded_file.save(save_path)
    # Initialize the chatbot agent
    chatbot = Agent(openai_api_key="Your_Api_Key")

    chatbot.ingest(save_path)

    user_query = "Describe the pdf"

    # Get the chatbot's response
    chatbot_response = chatbot.ask(user_query)

    # Display the chatbot's response
    print(chatbot_response)
    return jsonify({"result": chatbot_response})


    
if __name__ == '__main__':
    app.run(debug=True)

