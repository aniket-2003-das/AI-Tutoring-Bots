# import os
# import requests

# class WebQuery:
#     def __init__(self, perplexity_api_key=None) -> None:
#         self.perplexity_api_key = "Your_API_Key"
#         self.chain = None
#         self.db = None

#     def ask(self, question: str) -> str:
#         if self.chain is None:
#             response = "Please, add a document."
#         else:
#             docs = self.db.get_relevant_documents(question)
#             response = self.chain.run(input_documents=docs, question=question)
#         return response

#     def ingest(self, url: str) -> str:
#         # Fetch and extract content from the URL using the Perplexity API
#         content = self.fetch_and_extract(url)

#         # Create documents, split them, and create a retriever (placeholder code)
#         documents = [...]  # Create Document objects from 'content'
#         splitted_documents = [...]  # Split documents using 'self.text_splitter.split_documents'
#         self.db = [...]  # Create retriever using 'Chroma.from_documents'

#         # Load the question-answering chain (placeholder code)
#         self.chain = [...]  # Load the chain using 'load_qa_chain'

#         return "Success"

#     def fetch_and_extract(self, url: str) -> str:
#         api_url = "https://api.perplexity.ai/your-endpoint"  # Replace with the actual Perplexity API endpoint
#         headers = {
#             "accept": "application/json",
#             "content-type": "application/json",
#             "authorization": f"Bearer {self.perplexity_api_key}",
#         }

#         payload = {"url": url}
#         response = requests.post(api_url, json=payload, headers=headers)

#         if response.status_code == 200:
#             return response.json().get("content", "")
#         else:
#             raise Exception(f"Failed to fetch content. Status code: {response.status_code}")

#     def forget(self) -> None:
#         self.db = None
#         self.chain = None







# # Create an instance of WebQuery with your Perplexity API key
# web_query = WebQuery(perplexity_api_key="Your_API_Key")

# # Ingest a URL to add a document
# url_to_ingest = "https://en.wikipedia.org/wiki/Russo-Ukrainian_War"
# ingest_result = web_query.ingest(url_to_ingest)
# print(ingest_result)  # This should print "Success" if the ingestion is successful

# # Ask a question
# question_to_ask = "What is the main topic of the page?"
# response = web_query.ask(question_to_ask)
# print("Answer:", response)

# # Forget the documents and chain
# web_query.forget()

import requests

def AI_tutor():
    payload = {
        "model": "mistral-7b-instruct",
        "messages": [
            {
                "role": "system",
                "content": f"{personality}\n\n{my_information}\n\n{student_config}"
            },
            {
                "role": "user",
                "content": "/plan Mathematics"
            }
        ]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {ppxl_api_key}"
    }
    response = requests.post(url_ppxl, json=payload, headers=headers)
    data = response.json()
    answer = data['choices'][-1]['message']['content']
    print(answer)


# AI_tutor()