# webquery.py

import os
import trafilatura
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.docstore.document import Document

class WebQuery:
    def __init__(self, openai_api_key=None) -> None:
        if openai_api_key is None:
            # If openai_api_key is not provided, try to get it from the environment variable
            openai_api_key = os.environ.get("OPENAI_API_KEY")

        if openai_api_key is None:
            raise ValueError("OpenAI API key is missing. Please set the OPENAI_API_KEY environment variable.")

        self.embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        os.environ["OPENAI_API_KEY"] = openai_api_key
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self.llm = OpenAI(temperature=0, openai_api_key=openai_api_key, model_name="gpt-3.5-turbo-instruct")
        self.chain = None
        self.db = None

    def ask(self, question: str) -> str:
        if self.chain is None:
            response = "Please, add a document."
        else:
            docs = self.db.get_relevant_documents(question)
            response = self.chain.run(input_documents=docs, question=question)
        return response

    def ingest(self, url: str) -> str:
        result = trafilatura.extract(trafilatura.fetch_url(url))
        documents = [Document(page_content=result, metadata={"source": url})]
        splitted_documents = self.text_splitter.split_documents(documents)
        self.db = Chroma.from_documents(splitted_documents, self.embeddings).as_retriever()
        self.chain = load_qa_chain(OpenAI(temperature=0, openai_api_key=self.embeddings.api_key), chain_type="stuff")
        return "Success"

    def forget(self) -> None:
        self.db = None
        self.chain = None

