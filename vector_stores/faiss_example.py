# import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_huggingface import HuggingFaceEmbeddings


from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from pathlib import Path

# ----------------------------------------
# 1️⃣ Paths
# ----------------------------------------
pdf_dir = Path("/src/langchain-prebuilts/knowledge_bases/algorithm_textbooks_files")

# pdf_path   = "src/langchain-prebuilts/knowledge_bases/algorithm_textbooks_files/Algorithm Design - Kleinberg, Tardos.pdf"   # Your PDF file
store_path = "src/langchain-prebuilts/vector_stores/algorithm_textbooks/index"  # Folder to persist FAISS index
# "src\langchain-prebuilts\knowledge_bases\algorithm_textbooks_files\Algorithm Design - Kleinberg, Tardos.pdf"

# Chunk Each File
chunked_pdfs = []
for pdf_file in pdf_dir.rglob("*.pdf"):
    temp_list = []

    loader = PyPDFLoader(pdf_file)
    pages = loader.load()   # Each page is a Document object
    print("\nPDF loaded\n")
    for p in pages:
        # Split into smaller chunks (better embeddings & retrieval)
        splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=50)
        docs = splitter.split_documents(pages)
        
        chunk_dict={
        "filename": pdf_file,
        "page": p,
        "chunks": docs,
        }
        temp_list.append(chunk_dict)

    print("\nChunked\n")

    chunked_pdfs.append(temp_list)



# Initialize embeddings
embeddings = OpenAIEmbeddings()

# Create documents with metadata
documents = [
    Document(
        page_content="The quick brown fox jumps over the lazy dog.",
        metadata={"category": "animals", "source": "example_1"}
    ),
    Document(
        page_content="Cats are known for their independence.",
        metadata={"category": "animals", "source": "example_2"}
    ),
    Document(
        page_content="Dogs are often called man's best friend.",
        metadata={"category": "animals", "source": "example_3"}
    ),
]

# Create FAISS vector store from documents
vector_store = FAISS.from_documents(documents, embeddings)

# Perform a similarity search
query = "Tell me about animals."
results = vector_store.similarity_search(query, k=2)

# Print results including metadata
for doc in results:
    print("Content:", doc.page_content)
    print("Metadata:", doc.metadata)
    print("---")




# # ----------------------------------------
# # 2️⃣ Load & Split PDF
# # ----------------------------------------
# loader = PyPDFLoader(pdf_path)
# pages = loader.load()   # Each page is a Document object
# print("\nPDF loaded\n")

# # Split into smaller chunks (better embeddings & retrieval)
# splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=50)
# docs = splitter.split_documents(pages)
# print("\nChunked\n")
# print(f"{len(docs)}\n")
# # ----------------------------------------
# # 3️⃣ Embedding model
# # ----------------------------------------
# embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
# db = FAISS.load_local(store_path, embeddings, allow_dangerous_deserialization=True)
# print(db)
# # embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/Qwen3-Embedding-8B") #Qwen/
# print("Embedding created\n")
# print(f"{embeddings}\n")
# # ----------------------------------------
# # 4️⃣ Load existing FAISS store (or create new)
# # ----------------------------------------
# if os.path.exists(store_path):
#     # Load existing persistent index
#     db = FAISS.load_local(store_path, embeddings, allow_dangerous_deserialization=True)
#     print("✅ Loaded existing FAISS store.")
# else:
#     # Create a new FAISS index
#     # db = FAISS.from_texts([], embedding=embeddings)
#     db = FAISS.from_documents(docs, embedding=embeddings)
#     print("✅ Created new FAISS store.")

# # ----------------------------------------
# # 5️⃣ Add PDF documents to the vector store
# # ----------------------------------------
# db.add_documents(docs)
# db.save_local(store_path)
# print(f"✅ Added {len(docs)} chunks from {pdf_path} to {store_path}")

# # ----------------------------------------
# # 6️⃣ Query the updated store
# # ----------------------------------------
# query = "What is this PDF about?"
# results = db.similarity_search(query, k=2)
# print("\n🔎 Query:", query)
# for r in results:
#     print(f"• {r.page_content[:200]}...")











# import os
# from langchain_community.vectorstores import FAISS
# from langchain.embeddings import HuggingFaceEmbeddings

# # ---------------------------
# # 1️⃣ Create the embedding model
# # ---------------------------
# embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# # ---------------------------
# # 2️⃣ Sample documents
# # ---------------------------
# docs = [
#     "FAISS provides efficient similarity search.",
#     "LangChain integrates FAISS for vector storage.",
#     "Python is widely used in machine learning.",
#     "Transformers generate high-quality text embeddings.",
# ]

# # ---------------------------
# # 3️⃣ Create a FAISS vector store
# # ---------------------------
# vectorstore = FAISS.from_texts(texts=docs, embedding=embeddings)

# # ---------------------------
# # 4️⃣ Persist to disk
# # ---------------------------
# save_path = "faiss_store"
# vectorstore.save_local(save_path)
# print(f"✅ Vector store saved to: {save_path}")

# # ---------------------------
# # 5️⃣ Load it back later
# # ---------------------------
# loaded_store = FAISS.load_local(save_path, embeddings, allow_dangerous_deserialization=True)

# # ---------------------------
# # 6️⃣ Query the persistent store
# # ---------------------------
# query = "Which library is good for vector search?"
# results = loaded_store.similarity_search(query, k=2)

# print("\n🔎 Query:", query)
# for res in results:
#     print(f"  • {res.page_content}")

