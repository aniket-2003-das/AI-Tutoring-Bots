import fitz
from time import time as now
import cache
import feedback
import storage
import model
import css
import os
import base64
from streamlit_javascript import st_javascript


# BOILERPLATE

import streamlit as st
st.set_page_config(layout='centered', page_title="ED-2100 Pdf-Chatbot")
ss = st.session_state

# Initialize session state variables
if 'community_user' not in st.session_state:
    st.session_state['community_user'] = os.getenv('COMMUNITY_USER')

if 'data_dict' not in st.session_state:
    st.session_state['data_dict'] = {}

if 'debug' not in st.session_state:
    st.session_state['debug'] = {}

if 'fix_text' not in st.session_state:
    st.session_state['fix_text'] = None

if 'frag_size' not in st.session_state:
    st.session_state['frag_size'] = None
    
if 'model' not in st.session_state:
    st.session_state['model'] = None


st.write(f'<style>{css.v1}</style>', unsafe_allow_html=True)
header1 = st.empty()  # for errors / messages
header2 = st.empty()  # for errors / messages
header3 = st.empty()  # for errors / messages



# HANDLERS

def on_api_key_change():
    api_key = st.session_state.get('api_key') or os.getenv('OPENAI_KEY')
    if not api_key:
        return

    model.use_key(api_key)

    # Ensure that the 'data_dict' key is present in session state
    if 'data_dict' not in st.session_state:
        st.session_state['data_dict'] = {}

    try:
        # Attempt to create storage with the provided API key
        st.session_state['storage'] = storage.get_storage(
            api_key, data_dict=st.session_state['data_dict'])
    except Exception as e:
        st.error(f"Error creating storage: {e}")
        return

    st.session_state['cache'] = cache.get_cache()
    st.session_state['user'] = st.session_state['storage'].folder
    model.set_user(st.session_state['user'])
    st.session_state['feedback'] = feedback.get_feedback_adapter(
        st.session_state['user'])
    st.session_state['feedback_score'] = st.session_state['feedback'].get_score()

    st.session_state['debug']['storage.folder'] = st.session_state['storage'].folder
    st.session_state['debug']['storage.class'] = st.session_state['storage'].__class__.__name__


# COMPONENTS

def ui_api_key():
    if ss['community_user']:
        pct = model.community_tokens_available_pct()
        st.write(
            f'Tokens available: :{"green" if pct else "red"}[{int(pct)}%]')
        st.progress(pct/100)
        st.write('Refresh Time: ' + model.community_tokens_refresh_in())
        ss['community_pct'] = pct
        ss['debug']['community_pct'] = pct
    else:
        st.write('Enter your OpenAI API key')
        st.text_input('OpenAI API key', type='password', key='api_key',
                      on_change=on_api_key_change, label_visibility="collapsed")

def index_pdf_file():
    if ss['pdf_file']:
        ss['filename'] = ss['pdf_file'].name
        if ss['filename'] != ss.get('fielname_done'):  # UGLY
            with st.spinner(f'indexing {ss["filename"]}'):
                index = model.index_file(
                    ss['pdf_file'], ss['filename'], fix_text=ss['fix_text'], frag_size=ss['frag_size'], cache=ss['cache'])
                ss['index'] = index
                debug_index()
                ss['filename_done'] = ss['filename']  # UGLY

def debug_index():
    index = ss['index']
    d = {}
    d['hash'] = index['hash']
    d['frag_size'] = index['frag_size']
    d['n_pages'] = len(index['pages'])
    d['n_texts'] = len(index['texts'])
    d['summary'] = index['summary']
    d['pages'] = index['pages']
    d['texts'] = index['texts']
    d['time'] = index.get('time', {})
    ss['debug']['index'] = d

def ui_question():
    st.write('Ask questions' +
             (f' to {ss["filename"]}' if ss.get('filename') else ''))
    disabled = False
    st.text_area('question', key='question', height=100, placeholder='Enter question',
                 help='', label_visibility="collapsed", disabled=disabled)

def ui_hyde_answer():
    # TODO: enter or generate
    pass

def ui_output():
    output = ss.get('output', '')
    st.markdown(output)

def ui_debug():
    if ss.get('show_debug'):
        st.write('### debug')
        st.write(ss.get('debug', {}))

def b_ask():
    c1, c2, c3, c4, c5 = st.columns([2, 1, 1, 2, 2])
    if c2.button('👍', use_container_width=True, disabled=not ss.get('output')):
        ss['feedback'].send(+1, ss, details=ss['send_details'])
        ss['feedback_score'] = ss['feedback'].get_score()
    if c3.button('👎', use_container_width=True, disabled=not ss.get('output')):
        ss['feedback'].send(-1, ss, details=ss['send_details'])
        ss['feedback_score'] = ss['feedback'].get_score()
    score = ss.get('feedback_score', 0)
    c5.write(f'feedback score: {score}')
    c4.checkbox('send details', True, key='send_details',
                help='stored chat in database')
    # c1,c2,c3 = st.columns([1,3,1])
    # c2.radio('zzz',['👍',r'...',r'👎'],horizontal=True,label_visibility="collapsed")
    #
    disabled = (not ss.get('api_key') and not ss.get(
        'community_pct', 0)) or not ss.get('index')
    if c1.button('ASK', disabled=disabled, type='primary', use_container_width=True):
        question = ss.get('question', '')
        temperature = ss.get('temperature', 0.0)
        hyde = ss.get('use_hyde')
        hyde_prompt = ss.get('hyde_prompt')
        if ss.get('use_hyde_summary'):
            summary = ss['index']['summary']
            hyde_prompt += f" Context: {summary}\n\n"
        task = ss.get('task')
        max_frags = ss.get('max_frags', 1)
        n_before = ss.get('n_frag_before', 0)
        n_after = ss.get('n_frag_after', 0)
        index = ss.get('index', {})
        with st.spinner('preparing answer'):
            resp = model.query(question, index,
                               task=task,
                               temperature=temperature,
                               hyde=hyde,
                               hyde_prompt=hyde_prompt,
                               max_frags=max_frags,
                               limit=max_frags+2,
                               n_before=n_before,
                               n_after=n_after,
                               model=ss['text-davinci-003'],
                               )
        usage = resp.get('usage', {})
        usage['cnt'] = 1
        ss['debug']['model.query.resp'] = resp
        ss['debug']['resp.usage'] = usage
        ss['debug']['model.vector_query_time'] = resp['vector_query_time']

        q = question.strip()
        a = resp['text'].strip()
        ss['answer'] = a
        output_add(q, a)
        st.experimental_rerun()  # to enable the feedback buttons

def b_reindex():
    # TODO: disabled
    if st.button('reindex'):
        index_pdf_file()

def b_save():
    db = ss.get('storage')
    index = ss.get('index')
    name = ss.get('filename')
    api_key = ss.get('api_key')
    disabled = not api_key or not db or not index or not name
    help = "pdf stored for about 90 days if using individual API key."
    if st.button('save encrypted index ', disabled=disabled, help=help):
        with st.spinner('saving pdf'):
            db.put(name, index)

def b_delete():
    db = ss.get('storage')
    name = ss.get('selected_file')
    # TODO: confirm delete
    if st.button('delete pdf', disabled=not db or not name):
        with st.spinner('deleting pdf'):
            db.delete(name)
        # st.experimental_rerun()

def output_add(q, a):
    if 'output' not in ss:
        ss['output'] = ''
    q = q.replace('$', r'\$')
    a = a.replace('$', r'\$')
    new = f'#### {q}\n{a}\n\n'
    ss['output'] = new + ss['output']

def ui_pdf_file():
    st.sidebar.write('Upload or Select your Pdf File')
    disabled = not ss.get('user') or (not ss.get(
        'api_key') and not ss.get('community_pct', 0))
    t1, t2 = st.sidebar.tabs(['UPLOAD', 'SELECT'])
    with t1:
        uploaded_file = st.sidebar.file_uploader('pdf file', type='pdf', key='pdf_file',
                                         disabled=disabled, on_change=index_pdf_file, label_visibility="collapsed")
        b_save()
    with t2:
        filenames = ['']
        if ss.get('storage'):
            filenames += ss['storage'].list()
        def on_change():
            name = ss['selected_file']
            if name and ss.get('storage'):
                with ss['spin_select_file']:
                    with st.spinner('loading index'):
                        t0 = now()
                        index = ss['storage'].get(name)
                        ss['debug']['storage_get_time'] = now() - t0
                ss['filename'] = name  # XXX
                ss['index'] = index
                debug_index()
            else:
                # ss['index'] = {}
                pass
        st.sidebar.selectbox('select file', filenames, on_change=on_change,
                     key='selected_file', label_visibility="collapsed", disabled=disabled)
        b_delete()
        ss['spin_select_file'] = st.empty()
    return uploaded_file


def displayPDF(upl_file, width):
    if upl_file is not None:
        # Read file as bytes:
        bytes_data = upl_file.getvalue()

        # Convert to utf-8
        base64_pdf = base64.b64encode(bytes_data).decode("utf-8")

        # Embed PDF in HTML
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width={str(width)} height={str(width*4/3)} type="application/pdf"></iframe>'

        # Display file
        st.markdown(pdf_display, unsafe_allow_html=True)
    else:
        st.warning("Please upload a PDF file.")


def displayPDFpage(upl_file, page_nr):
    # Read file as bytes:
    bytes_data = upl_file.getvalue()

    # Convert to utf-8
    base64_pdf = base64.b64encode(bytes_data).decode("utf-8")

    # Embed PDF in HTML
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}#page={page_nr}" width="600" height="1000" type="application/pdf"></iframe>'

    # Display file
    st.markdown(pdf_display, unsafe_allow_html=True)


# Define the layout with 2 columns
container = st.container()
col1, col2 = container.columns((5.5, 4.5))

with st.sidebar:
	st.sidebar.header("Upload Section")
	ui_api_key()


# Column 1: PDF Upload
with col1:
    col1.header("Preview Section")
    st.subheader("Pdf Preview")
    ui_width = st_javascript("window.innerWidth")
    uploaded_file = ui_pdf_file()
    displayPDF(uploaded_file, ui_width)

# col2 : Chat section
with col2:
    col2.header("Chat Section")
    ui_question()
    ui_hyde_answer()
    b_ask()
    ui_output()
    ui_debug()


