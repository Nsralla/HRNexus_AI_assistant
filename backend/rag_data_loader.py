"""
RAG Data Loader Service for HR Nexus
=====================================
This module handles loading and processing markdown documentation files:
- Markdown files from the local kb/ folder
- Creates embeddings and saves to vector database (ChromaDB)

Usage:
    # Load data and create vector store:
    loader = RAGDataLoader()
    documents, split_docs, vectorstore = loader.load_and_create_vectorstore(
        persist_directory="./chroma_db"
    )

    # Query the vector store:
    results = vectorstore.similarity_search("What is the code review policy?", k=5)
"""
import json
import logging
from typing import List, Optional, Tuple
from pathlib import Path

# Check if vector database libraries are available
try:
    from langchain_cohere import CohereEmbeddings
    from langchain_chroma import Chroma
    HAS_VECTOR_DB = True
except ImportError:
    HAS_VECTOR_DB = False
    CohereEmbeddings = None
    Chroma = None

# LangChain imports
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RAGDataLoader:
    """
    Handles loading markdown documentation for RAG system
    """

    def __init__(
        self,
        kb_dir: str,
        chunk_size: int,
        chunk_overlap: int,
        embedding_model: str,
        collection_name: str
    ):
        """
        Initialize the RAG Data Loader

        Args:
            kb_dir: Directory containing markdown knowledge base files
            chunk_size: Size of text chunks for splitting
            chunk_overlap: Overlap between chunks
            embedding_model: HuggingFace model name for embeddings
            collection_name: Name for the ChromaDB collection
        """
        self.kb_dir = kb_dir
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embedding_model = embedding_model
        self.collection_name = collection_name

        # Get absolute path for kb directory
        self.base_dir = Path(__file__).parent
        self.kb_path = self.kb_dir

        # Initialize embedding and vector store
        self.embeddings = None
        self.vectorstore = None

        logger.info(f"RAGDataLoader initialized")
        logger.info(f"  KB directory: {self.kb_path}")

    def load_markdown_files(self, kb_dir: Optional[Path] = None) -> List[Document]:
        """
        Load Markdown files from knowledge base directory

        Args:
            kb_dir: Directory containing markdown files (defaults to self.kb_path)

        Returns:
            List of Document objects
        """
        kb_dir = kb_dir or self.kb_path
        documents = []

        # Ensure we have a Path object
        if isinstance(kb_dir, str):
            kb_dir = Path(kb_dir)

        # Check if directory exists
        if not kb_dir.exists():
            logger.warning(f"KB directory does not exist: {kb_dir}")
            return documents

        # Find all markdown files
        md_files = list(kb_dir.glob("*.md"))

        if not md_files:
            logger.warning(f"No markdown files found in {kb_dir}")
            return documents

        logger.info(f"Loading markdown files from {kb_dir}")

        for file_path in md_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                    # Extract title from markdown (first # heading)
                    title = self._extract_markdown_title(content) or file_path.stem

                    # Create Document with metadata
                    doc = Document(
                        page_content=content,
                        metadata={
                            "source": str(file_path),
                            "type": "markdown",
                            "filename": file_path.name,
                            "title": title,
                            "category": "knowledge_base"
                        }
                    )
                    documents.append(doc)
                    logger.debug(f"  Loaded: {file_path.name}")

            except Exception as e:
                logger.error(f"Error loading {file_path}: {e}")

        logger.info(f"Successfully loaded {len(documents)} markdown documents")
        return documents

    def load_all_documents(self) -> List[Document]:
        """
        Load all markdown documentation files

        Returns:
            List of Document objects
        """
        logger.info("=" * 80)
        logger.info("Loading documentation from markdown files")
        logger.info("=" * 80)

        # Load only Markdown files from kb folder
        md_docs = self.load_markdown_files()

        # Summary
        logger.info("=" * 80)
        logger.info(f"Total documents loaded: {len(md_docs)}")
        logger.info("=" * 80)

        return md_docs

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into smaller chunks for better retrieval

        Args:
            documents: List of Document objects to split

        Returns:
            List of split Document objects
        """
        if not documents:
            logger.warning("No documents to split")
            return []

        logger.info(f"Splitting {len(documents)} documents into chunks")
        logger.info(f"  Chunk size: {self.chunk_size}")
        logger.info(f"  Chunk overlap: {self.chunk_overlap}")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )

        split_docs = splitter.split_documents(documents)

        logger.info(f"Created {len(split_docs)} chunks from {len(documents)} documents")
        return split_docs

    def _extract_markdown_title(self, content: str) -> Optional[str]:
        """Extract the first # heading from markdown content"""
        lines = content.split('\n')
        for line in lines:
            if line.strip().startswith('# '):
                return line.strip()[2:].strip()
        return None

    def get_statistics(self, documents: List[Document]) -> dict:
        """
        Get statistics about loaded documents

        Args:
            documents: List of Document objects

        Returns:
            Dictionary with statistics
        """
        stats = {
            "total_documents": len(documents),
            "markdown_documents": sum(1 for d in documents if d.metadata.get("type") == "markdown"),
            "total_characters": sum(len(d.page_content) for d in documents),
            "average_chunk_size": sum(len(d.page_content) for d in documents) / len(documents) if documents else 0,
            "categories": {}
        }

        # Count by category
        for doc in documents:
            category = doc.metadata.get("category", "unknown")
            stats["categories"][category] = stats["categories"].get(category, 0) + 1

        return stats

    def initialize_embeddings(self):
        """
        Initialize the Cohere embeddings model

        Returns:
            CohereEmbeddings instance

        Raises:
            ImportError: If vector database libraries are not installed
        """
        if not HAS_VECTOR_DB:
            raise ImportError(
                "Vector database libraries not installed. "
                "Install with: pip install langchain-cohere langchain-chroma"
            )

        logger.info(f"Initializing Cohere embeddings model: {self.embedding_model}")

        # Use Cohere embeddings API (free tier available, no local RAM needed)
        self.embeddings = CohereEmbeddings(
            model=self.embedding_model,
            # API key will be loaded from environment variable COHERE_API_KEY
        )

        logger.info("Cohere embeddings initialized successfully")
        return self.embeddings

    def create_vector_store(
        self,
        documents: List[Document],
        persist_directory: Optional[str] = None
    ) -> Optional[Chroma]:
        """
        Create a vector store from documents with embeddings

        Args:
            documents: List of Document objects (should be split chunks)
            persist_directory: Optional directory to persist the vector store

        Returns:
            Chroma vector store instance or None if failed

        Raises:
            ImportError: If vector database libraries are not installed
        """
        if not HAS_VECTOR_DB:
            raise ImportError(
                "Vector database libraries not installed. "
                "Install with: pip install langchain-huggingface langchain-chroma torch sentence-transformers"
            )

        if not documents:
            logger.warning("No documents to create vector store")
            return None

        # Initialize embeddings if not already done
        if self.embeddings is None:
            self.initialize_embeddings()

        logger.info("=" * 80)
        logger.info("Creating vector store")
        logger.info("=" * 80)
        logger.info(f"Processing {len(documents)} document chunks")

        try:
            # Create vector store
            if persist_directory:
                persist_path = Path(persist_directory)
                persist_path.mkdir(parents=True, exist_ok=True)

                self.vectorstore = Chroma.from_documents(
                    documents=documents,
                    embedding=self.embeddings,
                    collection_name=self.collection_name,
                    persist_directory=str(persist_path)
                )
                logger.info(f"Vector store created and persisted to: {persist_path}")
            else:
                self.vectorstore = Chroma.from_documents(
                    documents=documents,
                    embedding=self.embeddings,
                    collection_name=self.collection_name
                )
                logger.info("Vector store created (in-memory)")

            logger.info(f"  Collection name: {self.collection_name}")
            logger.info(f"  Total chunks: {len(documents)}")
            logger.info("=" * 80)

            return self.vectorstore

        except Exception as e:
            logger.error(f"Failed to create vector store: {e}")
            return None

    def load_and_create_vectorstore(
        self,
        persist_directory: Optional[str] = None
    ) -> Tuple[List[Document], List[Document], Optional[Chroma]]:
        """
        Complete pipeline: Load documents, create embeddings, and save to vector database

        Args:
            persist_directory: Optional directory to persist the vector store

        Returns:
            Tuple of (documents, split_docs, vectorstore)
        """
        logger.info("=" * 80)
        logger.info("RAG DATA LOADER - Complete Pipeline")
        logger.info("=" * 80)

        # Step 1: Load all documents
        documents = self.load_all_documents()

        if not documents:
            logger.warning("No documents loaded. Pipeline aborted.")
            return ([], [], None)

        # Step 2: Split documents
        split_docs = self.split_documents(documents)

        if not split_docs:
            logger.warning("No document chunks created. Pipeline aborted.")
            return (documents, [], None)

        # Step 3: Create vector store with embeddings
        vectorstore = self.create_vector_store(split_docs, persist_directory=persist_directory)

        # Final summary
        logger.info("=" * 80)
        logger.info("Pipeline Complete")
        logger.info("=" * 80)
        logger.info(f"Documents loaded: {len(documents)}")
        logger.info(f"Chunks created: {len(split_docs)}")
        logger.info(f"Vector store: {'Ready' if vectorstore else 'Failed'}")
        logger.info("=" * 80)

        return (documents, split_docs, vectorstore)

    def load_existing_vectorstore(
        self,
        persist_directory: str
    ) -> Optional[Chroma]:
        """
        Load an existing persisted vector store

        Args:
            persist_directory: Directory where vector store is persisted

        Returns:
            Chroma vector store instance or None if not found
        """
        if not HAS_VECTOR_DB:
            raise ImportError(
                "Vector database libraries not installed. "
                "Install with: pip install langchain-huggingface langchain-chroma torch sentence-transformers"
            )

        persist_path = Path(persist_directory)

        if not persist_path.exists():
            logger.warning(f"Persist directory does not exist: {persist_path}")
            return None

        # Initialize embeddings if not already done
        if self.embeddings is None:
            self.initialize_embeddings()

        try:
            logger.info(f"Loading existing vector store from: {persist_path}")

            self.vectorstore = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=str(persist_path)
            )

            logger.info("Vector store loaded successfully")
            return self.vectorstore

        except Exception as e:
            logger.error(f"Failed to load vector store: {e}")
            return None


def main():
    """
    Script to rebuild vector store with markdown files only
    """
    import os

    kb_dir = os.path.join(os.path.dirname(__file__), "sources/kb")

    print("[INFO] KB Directory:", kb_dir)

    # Initialize loader
    loader = RAGDataLoader(
        kb_dir=kb_dir,
        chunk_size=1000,
        chunk_overlap=350,
        embedding_model="sentence-transformers/all-MiniLM-L6-v2",
        collection_name="hr_nexus_rag"
    )

    # Run complete pipeline with persistent storage
    documents, split_docs, vectorstore = loader.load_and_create_vectorstore(
        persist_directory="./chroma_db"
    )

    # Get statistics
    if split_docs:
        stats = loader.get_statistics(split_docs)
        logger.info("\nStatistics:")
        logger.info(json.dumps(stats, indent=2))

    # Test vector store with a query
    if vectorstore:
        logger.info("\nTesting vector store with sample query...")
        try:
            results = vectorstore.similarity_search("What is the code review policy?", k=3)
            logger.info(f"Retrieved {len(results)} relevant documents")

            for i, doc in enumerate(results, 1):
                logger.info(f"\n  [{i}] {doc.metadata.get('filename')} ({doc.metadata.get('type')})")
                preview = doc.page_content[:100].replace('\n', ' ')
                logger.info(f"      Preview: {preview}...")
        except Exception as e:
            logger.error(f"Error querying vector store: {e}")

    return vectorstore


if __name__ == "__main__":
    main()
