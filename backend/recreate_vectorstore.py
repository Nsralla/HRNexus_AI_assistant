"""
Script to recreate the ChromaDB vector store with Cohere embeddings
Run this after changing embedding models to avoid dimension mismatch errors
"""
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add backend to path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from rag_data_loader import RAGDataLoader

def main():
    print("=" * 80)
    print("Recreating Vector Store with Cohere Embeddings")
    print("=" * 80)

    # Initialize RAG loader with Cohere embeddings
    rag_loader = RAGDataLoader(
        kb_dir="sources/kb",
        chunk_size=1000,
        chunk_overlap=350,
        embedding_model="embed-english-v3.0",  # Cohere free embedding model
        collection_name="hr_nexus_rag"
    )

    # Load documents and create vector store
    print("\nLoading documents and creating vector store...")
    documents, split_docs, vectorstore = rag_loader.load_and_create_vectorstore(
        persist_directory="./chroma_db"
    )

    if vectorstore:
        print("\n" + "=" * 80)
        print("SUCCESS! Vector store created successfully")
        print("=" * 80)
        print(f"Documents loaded: {len(documents)}")
        print(f"Document chunks: {len(split_docs)}")
        print(f"Embedding model: {rag_loader.embedding_model}")
        print(f"Persist directory: ./chroma_db")

        # Test a simple query
        print("\nTesting vector store with a sample query...")
        results = vectorstore.similarity_search("employee", k=2)
        print(f"Found {len(results)} results for test query")

        return 0
    else:
        print("\n" + "=" * 80)
        print("ERROR: Failed to create vector store")
        print("=" * 80)
        return 1

if __name__ == "__main__":
    sys.exit(main())
