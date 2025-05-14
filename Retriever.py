from langchain_huggingface import HuggingFaceEmbeddings
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_faiss_index(embeddings, documents):
    # Create a FAISS index from the documents and embeddings
    vector_store = FAISS.from_documents(documents, embeddings)
    
    # Create a retriever from the vector store
    retriever = vector_store.as_retriever()

    # Cortar documentos muito grandes
    all_splits = splitDocuments(documents)
    document_ids = vector_store.add_documents(documents=all_splits)
    
    return retriever

def splitDocuments(documents):
    # Split the documents into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # chunk size (characters)
    chunk_overlap=200,  # chunk overlap (characters)
    add_start_index=True,  # track index in original document
)
    all_splits = text_splitter.split_documents(documents)
    
    return all_splits

def importFaiss():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

    loader = CSVLoader(file_path="Dados\DadosLimpos.csv", encoding="utf-8")
    documents = loader.load()

    retriever = create_faiss_index(embeddings, documents)

    return retriever

if __name__ == "__main__":
    retriever = importFaiss()
    print(retriever.invoke("Bolo de fubá"))