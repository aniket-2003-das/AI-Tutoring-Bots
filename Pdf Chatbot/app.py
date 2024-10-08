import base64
import os
import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
from streamlit_javascript import st_javascript
from openai.error import OpenAIError

from utils import (
    text_split,
    parse_pdf,
    get_embeddings,
    get_sources,
    get_answer,
    get_condensed_question,
    get_answers_bis,
)
load_dotenv()
os.environ["OPENAI_API_KEY"] = "Your_Api_Key"
openai_api_key = os.getenv("OPENAI_API_KEY")
st.set_page_config(page_title="ED2100 Chat with Pdf", layout="wide")
st.header("ED2100 Chat with PDF")

if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []


def clear_submit():
    st.session_state["submit"] = False


def displayPDF(upl_file, width):
    # Read file as bytes:
    bytes_data = upl_file.getvalue()

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

with st.sidebar:
   
    model_name = "gpt-3.5-turbo"
    # model_name = st.radio(
    #     "Select the model", ("gpt-3.5-turbo", "text-davinci-003", "gpt-4")
    # )

    approach = "1"
    # approach = st.radio(
    #     "Choose an approach", ("1", "2"))

    uploaded_file = st.file_uploader(
        "Upload a Pdf file",
        type=["pdf"],
        help="Only PDF files are supported",
        on_change=clear_submit,
    )


col1, col2 = st.columns(spec=[6, 4], gap="small")

with col1:
    st.write("Preview Section : Upload Pdf File to get Preview.")

with col2:
    st.write("Chat Section : Ask a question to start a chat.")
    question = st.text_input(
    "Ask about the file",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_file,
    on_change=clear_submit,
)
    st.write("ED2100 Chat Log :")


if uploaded_file:
    with col1:
        ui_width = st_javascript("window.innerWidth")
        displayPDF(uploaded_file, ui_width)

    with col2:
        pdf_document = parse_pdf(uploaded_file)
        text = text_split(pdf_document)
        try:
            vs = get_embeddings(text, openai_api_key)
            st.session_state["api_key_configured"] = True
        except OpenAIError as e:
            st.error(e._message)


        if uploaded_file and question and openai_api_key:
            try:
                if approach == 1:
                    chat_history_tuples = [
                    (st.session_state["past"][i], st.session_state["generated"][i])
                    for i in range(len(st.session_state["generated"]))
                    ]
                    condensed_question = get_condensed_question(
                        question, chat_history_tuples, model_name, openai_api_key
                    )
                    sources = get_sources(vs, condensed_question)
                    answer = get_answer(sources, condensed_question, openai_api_key)
                    st.session_state.generated.append(answer["output_text"])
                else:
                    answer = get_answers_bis(vs,question,model_name,openai_api_key,st.session_state)
                    st.session_state.generated.append(answer["answer"])
                
                st.session_state.past.append(question)

                # for source in sources:
                #    st.markdown(source.page_content)
                #    st.markdown(source.metadata["source"])
                #    st.markdown("---")

            except OpenAIError as e:
                st.error(e._message)

            if st.session_state["generated"]:
                for i in range(len(st.session_state["generated"]) - 1, -1, -1):
                    message(
                        st.session_state["past"][i],
                        is_user=True,
                        avatar_style="initials",
                        seed="User",
                        key=str(i) + "_user",
                    )
                    message(
                        st.session_state["generated"][i],
                        avatar_style="initials",
                        seed="ED2100",
                        key=str(i),
                    )




# streamlit run app.py