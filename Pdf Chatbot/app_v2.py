import os
import base64
from streamlit_javascript import st_javascript
import pull_requests
from datetime import datetime
import tempfile
import streamlit as st
from streamlit_chat import message
from agent import Agent
from dotenv import load_dotenv
import openai
import json 
import pymongo



load_dotenv()
os.environ["OPENAI_API_KEY"] = "Your_Api_Key"
openai_api_key = os.getenv("OPENAI_API_KEY")
st.set_page_config(page_title="ED2100 Chat with Pdf", layout="wide")



mongodb_url = "Mongo_cluster_url"
client = pymongo.MongoClient(mongodb_url)
db = client["ED2100"]
collection1_name = db["quizlog2"]
collection2_name = db["chatlog"]



# Function to check if OPENAI_API_KEY is set
def is_openai_api_key_set() -> bool:
    return len(st.session_state.get("OPENAI_API_KEY", "Your_Api_Key")) > 0



# Initialize OPENAI_API_KEY if not set
if "OPENAI_API_KEY" not in st.session_state:
    st.session_state["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY", "Your_Api_Key")

if "saved_files" not in st.session_state:
    st.session_state["saved_files"] = set()

# Initialize messages if not set
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Initialize agent if not set
if "agent" not in st.session_state:
    if is_openai_api_key_set():
        st.session_state["agent"] = Agent(st.session_state["OPENAI_API_KEY"])
    else:
        st.session_state["agent"] = None

# Initialize user input if not set
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""

# Initialize ingestion_spinner if not set
if "ingestion_spinner" not in st.session_state:
    st.session_state["ingestion_spinner"] = st.empty()

# Initialize thinking_spinner if not set
if "thinking_spinner" not in st.session_state:
    st.session_state["thinking_spinner"] = st.empty()



def get_quiz_json (prompt, openai_api_key):
    openai.api_key = openai_api_key
    # Define the OpenAI prompt for generating quiz questions
    quiz_prompt = f"{prompt}\n"
    # Call the OpenAI API to generate quiz questions
    response = openai.Completion.create(
        engine="text-davinci-003",  # You can adjust the engine based on your needs
        prompt=quiz_prompt,
        temperature=0.7,  # Adjust the temperature parameter for more controlled or creative responses
        max_tokens=1500,  # Adjust the max_tokens parameter to limit the response length
        stop=None  # You can provide a list of stop sequences to control the response
    )
    # Extract and return the generated text
    generated_text = response["choices"][0]["text"]
    print(generated_text)
    generated_dict = json.loads(generated_text)
    print (generated_dict)
    collection1_name.insert_one(generated_dict)
    return generated_text

def get_chat_log():
    # Fetch all documents from the chatlog collection
    chat_logs = collection2_name.find()
    return chat_logs

def display_messages():
    for i, (msg, is_user) in enumerate(st.session_state["messages"]):
        message(msg, is_user=is_user, key=str(i))
    st.session_state["thinking_spinner"] = st.empty()

def insert_chat_log(messages, uploaded_files):
    teacherId = pull_requests.id()
    chat_entry = {
        "teacherId": teacherId,
        "timestamp": datetime.utcnow(),
        "interaction": []  # List to store user-agent interactions
    }

    for user_msg, is_user in messages:
        for uploaded_file in uploaded_files:
            interaction_entry = {
                "uploaded_file": uploaded_file.name,
                "user_message": user_msg if is_user else None,
                "agent_message": user_msg if not is_user else None,
            }
            chat_entry["interaction"].append(interaction_entry)

    if chat_entry["interaction"]:  # Only insert if there's at least one interaction
        collection2_name.insert_one(chat_entry)

def process_input():
    if st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
        user_text = st.session_state["user_input"].strip()
        with st.session_state["thinking_spinner"], st.spinner(f"Thinking"):
            agent_text = st.session_state["agent"].ask(user_text)
        st.session_state["messages"].append((user_text, True))
        st.session_state["messages"].append((agent_text, False))
        insert_chat_log(st.session_state["messages"], st.session_state["file_uploader"])

def read_and_save_file():
    st.session_state["agent"].forget()  # to reset the knowledge base
    st.session_state["messages"] = []
    st.session_state["user_input"] = ""
    for file in st.session_state["file_uploader"]:
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tf.write(file.getbuffer())
            file_path = tf.name
        with st.session_state["ingestion_spinner"], st.spinner(f"Ingesting {file.name}"):
            st.session_state["agent"].ingest(file_path)
        os.remove(file_path)

def is_openai_api_key_set() -> bool:
    return len(st.session_state["OPENAI_API_KEY"]) > 0

def displayPDF(uploaded_files, width):
    for file_content in uploaded_files:
        # If file_content is a file-like object (uploaded file), read its content
        bytes_data = file_content.getvalue()
        # Convert to utf-8
        base64_pdf = base64.b64encode(bytes_data).decode("utf-8")
        # Embed PDF in HTML
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width={str(width)} height={str(width*4/3)} type="application/pdf"></iframe>'
        # Display file
        st.markdown(pdf_display, unsafe_allow_html=True)

def displayPDFpage(upl_file, page_nr):
    # Read file as bytes:
    bytes_data = upl_file.getvalue()
    # Convert to utf-8
    base64_pdf = base64.b64encode(bytes_data).decode("utf-8")
    # Embed PDF in HTML
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}#page={page_nr}" width="600" height="1000" type="application/pdf"></iframe>'
    # Display file
    st.markdown(pdf_display, unsafe_allow_html=True)




if len(st.session_state) == 0:
    st.session_state["messages"] = []
    st.session_state["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY", "Your_Api_Key")
    if is_openai_api_key_set():
        st.session_state["agent"] = Agent(st.session_state["OPENAI_API_KEY"])
    else:
        st.session_state["agent"] = None



st.header("ED2100 Chat with PDF")
st.divider()
with st.sidebar:
    st.header("SIDEBAR")
    st.divider()
    st.write("File section :-")
    t1, t2, t3 = st.sidebar.tabs(['UPLOAD PDF', 'SELECT PDF', 'GENERATE QUIZ'])
    with t1:
        st.write("Upload a pdf file -:")
        model_name = "gpt-3.5-turbo"
        approach = "1"
        uploaded_file = st.file_uploader(
            "Upload document",
            type=["pdf"],
            key="file_uploader",
            on_change=read_and_save_file,
            label_visibility="collapsed",
            accept_multiple_files=True,
            disabled=not is_openai_api_key_set(),
        )
        st.session_state["ingestion_spinner"] = st.empty()
        if uploaded_file:
            for file in uploaded_file:
                if file.name not in st.session_state["saved_files"]:
                    st.session_state["saved_files"].add(file.name)
    with t2:
        st.write("PDF Dropdown :-")
        selected_file = st.selectbox("Select a PDF from uploaded ones.", [
                                     ""] + list(st.session_state["saved_files"]), index=0 if uploaded_file else None, help="Select a saved file to view past chats.")
    with t3:
        st.write("Customize Quiz -:")
        # # Input fields for quiz parameters
        teacherId = pull_requests.id()
        # Input fields for quiz parameters
        topic = st.text_input("Topic -:", placeholder="Enter topic name")
        # Subject Name
        subject_name_options = ["Select a subject.", "Physics", "Chemistry", "Mathematics"]
        subject_name_placeholder = st.selectbox("Subject Dropdown -:", subject_name_options, index=0, help="Select subject that fits best to the pdf")
        subject_name = subject_name_placeholder if subject_name_placeholder != "" else None
        # Difficulty Level
        difficulty_options = ["Select a difficulty level.", "Easy Difficulty", "Medium Difficulty", "Hard Difficulty"]
        difficulty_level_placeholder = st.selectbox("Choose Difficulty -:", difficulty_options, index=0, help="Select difficulty level for the quiz")
        difficulty_level = difficulty_level_placeholder if difficulty_level_placeholder != "" else None
        # Duration
        duration_options = ["5 minutes", "10 minutes", "30 minutes"]
        duration_placeholder = st.selectbox("Time Duration 5 minutes (Default) -:", duration_options, index=0, help="Select time duration to complete Quiz")
        duration = duration_placeholder if duration_placeholder != "" else None
        # duration = "5 min"
        current_time = datetime.utcnow()
        if st.button("Generate Quiz"):
            prompt1 = f"""Create a very detailed teacher\'s quiz for {topic} that focuses on {subject_name} with difficulty level {difficulty_level}, type: MCQ and true/false. If takes no more than {duration} to complete. Return a JSON with double quotes with the following properties: 
            topic, difficulty_level, duration, subject_name, title, description, teacherId = {teacherId}, created_At = {current_time}, createdBy = "AI", Modified_At = {current_time}, questionImage = Boolean False ,status = Boolean False, visibility = Boolean False, assignedQuizesToClasses = Boolean False type, questions;
            questions will have the properties as follows:   
            questionName , option1,  option2, option3, option4, explanation, answer note answer will be the value of the correct option and "type" of question is must field. Explanation will be string with a small explanation of the answer of the question. if question type is True/False give only two options option1 and option2 
            with value of True and False of option1 and option2  else questionName, option1,  option2, option3, option4,  answer, duration, description."""
            with st.spinner("Generating Quiz..."):
                get_quiz_json(prompt=prompt1, openai_api_key = openai_api_key)



col1, col2 = st.columns(spec=[5, 5], gap="small")
with col1:
    st.write("Preview Section :- Upload Pdf File to get Preview.")
    st.divider()
    ui_width = st_javascript("window.innerWidth")
    displayPDF(uploaded_file, width= ui_width)
with col2:
    st.write("Chat Section :- Ask a question to start a chat.")
    st.divider()
    question = st.text_input("Ask about the file", key="user_input",placeholder="Can you give me a short summary?", disabled=not is_openai_api_key_set(), on_change=process_input)
    st.divider()
    st.write("Current Messages :-")
    st.divider()
    display_messages()
    st.divider()
    st.write("ED2100 Chat Log :-")
    st.divider()



if selected_file:
    with col2:
        # Display past chats
        past_chats = get_chat_log()
        # Display past chats
        past_chats = get_chat_log()
        for chat_entry in past_chats:
            interactions = chat_entry.get("interaction", [])
            for interaction in interactions:
                if interaction.get("user_message"):
                    message(interaction["user_message"], is_user=True)
                if interaction.get("agent_message"):
                    message(interaction["agent_message"], is_user=False)
        st.divider()


# streamlit run app_v2.py