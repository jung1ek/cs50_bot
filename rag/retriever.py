from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever

# setup RAG vector database
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                  model_kwargs={"device": "cpu"})
vectore_store = Chroma(
    collection_name="cs50_policy",
    embedding_function=embeddings,
    persist_directory="rag/chroma_db"
)
vector_retriever = vectore_store.as_retriever(search_kwargs={"k":1})
bm_retriever = BM25Retriever.from_texts(vectore_store._collection.get()["documents"])
bm_retriever.k = 1

def get_retriever():
    retriever = EnsembleRetriever(
        retrievers=[vector_retriever,bm_retriever],
        weights=[0.4,0.6]
    )
    return retriever