# services/querying.py

import requests
import sys
import subprocess
from langchain_community.vectorstores import FAISS

class LLMQueryService:
    def __init__(self, vector_store, groq_api_key, openai_api_key, model_var, provider_var):
        self.vector_store = vector_store
        self.groq_api_key = groq_api_key
        self.openai_api_key = openai_api_key
        self.model_var = model_var
        self.provider_var = provider_var
        self.messages = []

    def query_documents_and_llm(self, query):
        if self.vector_store is None:
            return "No documents have been loaded. Please choose a folder first.", "N/A"
        relevant_docs = self.vector_store.similarity_search(query, k=5)
        doc_context = " ".join([doc.page_content for doc in relevant_docs])
        # Append the user message with context
        self.messages.append({"role": "user", "content": f"Based on the following documents: {doc_context}\n\n{query}"})
        # Keep only the last N messages
        MAX_CONVERSATION_LENGTH = 10
        if len(self.messages) > MAX_CONVERSATION_LENGTH:
            self.messages = self.messages[-MAX_CONVERSATION_LENGTH:]
        provider = self.provider_var.get()
        if provider == 'Groq':
            assistant_response = self.query_groq_llm()
        elif provider == 'OpenAI':
            assistant_response = self.query_openai_llm()
        else:
            assistant_response = "No provider selected."
        # Append assistant's response to messages
        self.messages.append({"role": "assistant", "content": assistant_response})
        # Collect all unique sources
        sources = list(set([doc.metadata.get('source', 'Unknown source') for doc in relevant_docs]))
        return assistant_response, sources

    def query_groq_llm(self):
        headers = {
            'Authorization': f'Bearer {self.groq_api_key}',
            'Content-Type': 'application/json',
        }
        data = {
            "model": self.model_var.get(),
            "messages": self.messages,
            "temperature": 0.7,
            "max_tokens": 1000
        }
        response = requests.post('https://api.groq.com/openai/v1/chat/completions', json=data, headers=headers)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Error: {response.status_code} - {response.text}"

    def query_openai_llm(self):
        headers = {
            'Authorization': f'Bearer {self.openai_api_key}',
            'Content-Type': 'application/json',
        }
        data = {
            "model": self.model_var.get(),
            "messages": self.messages,
            "temperature": 0.7,
            "max_tokens": 1000
        }
        response = requests.post('https://api.openai.com/v1/chat/completions', json=data, headers=headers)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Error: {response.status_code} - {response.text}"
