import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import YoutubeLoader
from langchain.llms import OpenAI
from langchain.docstore.document import Document

class YoutubeQuery:
    def __init__(self, openai_api_key = None) -> None:
        self.embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        os.environ["OPENAI_API_KEY"] = "Your_API_Key"
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self.llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
        self.chain = None
        self.db = None

    def ask(self, question: str) -> str:
        if self.chain is None:
            response = "Please, add a video."
        else:
            docs = self.db.get_relevant_documents(question)
            response = self.chain.run(input_documents=docs, question=question)
        return response

    def ingest(self, url: str) -> str:
        documents = YoutubeLoader.from_youtube_url(url, add_video_info=False).load()
        splitted_documents = self.text_splitter.split_documents(documents)
        self.db = Chroma.from_documents(splitted_documents, self.embeddings).as_retriever()
        self.chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")
        return "Success"

    def forget(self) -> None:
        self.db = None
        self.chain = None




