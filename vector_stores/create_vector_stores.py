
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_openai import OpenAIEmbeddings
# from tqdm import tqdm
# import time
# from langchain_core.documents import Document


import os
from pathlib import Path
import json
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


# # ----------------------------------------
# # Config
# # ----------------------------------------
## Set TRUE To Reset Vector Store
reset = False


# # ----------------------------------------
# # Paths
# # ----------------------------------------
pdf_dir = Path("./knowledge_stores") 
save_path = "./vector_stores"
store_path = f'{save_path}/index'

# # ----------------------------------------
# # Embedding model
# # ----------------------------------------
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
# embeddings = OpenAIEmbeddings()

# # ----------------------------------------
# # Load, Split, Chunk, Save
# # ----------------------------------------
chunked_pdfs = []
chunked_docs = []
# Chunk Each File
for pdf_file in pdf_dir.rglob('*.pdf'):
    print(f'\nLoading: {pdf_file}')
    temp_list = []

    loader = PyPDFLoader(pdf_file)
    pages = loader.load()   # Each page is a Document object
    print(f"PDF loaded. Total pages: {len(pages)}")

    for i, page in enumerate(pages):
        try:
            # Split into smaller chunks (better embeddings & retrieval)
            splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=50)
            docs = splitter.split_documents([page])
            for c, doc in enumerate(docs):     
                chunk_dict={
                "filename": str(pdf_file).split('\\')[-1],
                "page_num": i,
                "chunk_num": c,
                "content": doc.page_content
                }
                temp_list.append(chunk_dict)
                chunked_docs.append(doc)
        except:
            print(f'skipped page {i}')
        
    print(f"Chunks: {len(temp_list)}\n")

    chunked_pdfs = chunked_pdfs + temp_list

# Save to JSON
filename = f'{save_path}/chunked_pdfs.json'
with open(filename, 'w') as f:
    json.dump(chunked_pdfs, f, indent=4)
print(f"Saved to {filename}\n")

# # ----------------------------------------
# # Load existing FAISS store (or create new), and add documents
# # ----------------------------------------

if os.path.exists(store_path) and not reset:
    # Load existing persistent index
    vector_store = FAISS.load_local(store_path, embeddings, allow_dangerous_deserialization=True)
    print("✅ Loaded existing FAISS store.")
    vector_store.add_documents(chunked_docs)
    vector_store.save_local(store_path)
    print(f"✅ Added {len(chunked_docs)} chunks from {pdf_dir} to {store_path}")
else:
    # Create a new FAISS index
    # vector_store = FAISS.from_texts([], embedding=embeddings)
    vector_store = FAISS.from_documents(chunked_docs, embedding=embeddings)
    vector_store.save_local(store_path)
    print("✅ Created new FAISS store.")
    print(f"✅ Added {len(chunked_docs)} chunks from {pdf_dir} to {store_path}")

# Perform a similarity search
query = "Tell me about algorithms."
new_vector_store = FAISS.load_local(
    store_path, embeddings, allow_dangerous_deserialization=True
)

results = vector_store.similarity_search(query, k=5)
for i in results:
    print(f'Doc {i}:\n  {i.page_content}\n')

