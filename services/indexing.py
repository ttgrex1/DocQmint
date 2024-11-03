# services/indexing.py

import os
import numpy as np
import faiss
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore

class DocumentIndexer:
    def __init__(self):
        self.embedding = OpenAIEmbeddings()
        self.docstore = InMemoryDocstore({})
        self.index = None
        self.vector_store = None
        self.splitter = RecursiveCharacterTextSplitter()

    def index_documents(self, folder_path):
        # Reset docstore and index
        self.docstore = InMemoryDocstore({})
        self.index = None

        documents = self.load_documents(folder_path)
        if not documents:
            raise ValueError("No documents found in the selected folder.")

        split_docs = self.splitter.split_documents(documents)
        texts = [doc.page_content for doc in split_docs]

        # Create embeddings and index the documents
        doc_embeddings = self.batch_embed_documents(texts, batch_size=5)

        # Prepare FAISS index
        embedding_size = len(doc_embeddings[0]) if doc_embeddings else 0
        self.index = faiss.IndexFlatL2(embedding_size)
        for i, emb in enumerate(doc_embeddings):
            self.index.add(np.array([emb]).astype('float32'))
            self.docstore.add({str(i): split_docs[i]})

        self.vector_store = FAISS(
            embedding_function=self.embedding,
            index=self.index,
            docstore=self.docstore,
            index_to_docstore_id={i: str(i) for i in range(len(split_docs))}
        )

    def load_documents(self, folder_path):
        documents = []
        for filename in os.listdir(folder_path):
            filepath = os.path.join(folder_path, filename)
            if filename.lower().endswith('.pdf'):
                loader = PyPDFLoader(filepath)
                documents.extend(loader.load())
            else:
                loader = DirectoryLoader(folder_path, glob=filename)
                documents.extend(loader.load())
        return documents

    def batch_embed_documents(self, texts, batch_size):
        batches = [texts[i:i + batch_size] for i in range(0, len(texts), batch_size)]
        all_embeddings = []
        for batch in batches:
            batch_embeddings = self.embedding.embed_documents(batch)
            all_embeddings.extend(batch_embeddings)
        return all_embeddings

    def load_vector_store(self, index_folder):
        self.vector_store = FAISS.load_local(index_folder, self.embedding)
        self.index = self.vector_store.index
        self.docstore = self.vector_store.docstore
