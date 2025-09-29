from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def vs_search(query: str, search_num: int):
    """
    Similarity search against a FAISS vector store.
    Returns top 'search_num' results as a string.
    """
    store_path="./vector_stores/index"
    embeddings=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vector_store = FAISS.load_local(
    store_path, embeddings, allow_dangerous_deserialization=True
    )
    results = vector_store.similarity_search(query, k=search_num)
    result_str =''
    for i in results:
        pdf_source = i.metadata.get("source").split('\\')[-1].split('.')[0]
        result_str = result_str + f'Doc Source: {pdf_source}, Page: {i.metadata.get('page')}\nContent: {i.page_content}\n\n\n'
    return result_str