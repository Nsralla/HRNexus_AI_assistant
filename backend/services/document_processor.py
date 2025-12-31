"""
Document Processing Service for HR Nexus
=========================================
Handles file upload, text extraction, chunking, embedding, and storage in ChromaDB.

Features:
- Support for multiple file types (TXT, MD, JSON, CSV, PDF)
- Text extraction and cleaning
- Document chunking with overlap
- Embedding generation using Cohere
- Storage in existing ChromaDB vector store
- Metadata tracking in PostgreSQL
"""
import os
import json
import logging
import hashlib
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime

# LangChain imports
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_cohere import CohereEmbeddings
from langchain_chroma import Chroma

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DocumentProcessor:
    """
    Processes uploaded documents and adds them to the vector database
    """

    def __init__(
        self,
        chroma_persist_dir: str = "./chroma_db",
        collection_name: str = "hr_nexus_rag",
        embedding_model: str = "embed-english-v3.0",
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        upload_dir: str = "./uploads"
    ):
        """
        Initialize the Document Processor

        Args:
            chroma_persist_dir: Directory where ChromaDB is persisted
            collection_name: Name of the ChromaDB collection
            embedding_model: Cohere embedding model name
            chunk_size: Size of text chunks for splitting
            chunk_overlap: Overlap between chunks
            upload_dir: Directory to store uploaded files
        """
        self.chroma_persist_dir = chroma_persist_dir
        self.collection_name = collection_name
        self.embedding_model = embedding_model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.upload_dir = upload_dir

        # Ensure upload directory exists
        Path(upload_dir).mkdir(parents=True, exist_ok=True)

        # Initialize embeddings
        self.embeddings = CohereEmbeddings(
            model=embedding_model,
            # API key loaded from COHERE_API_KEY environment variable
        )

        # Load existing vector store
        self.vectorstore = None
        self._load_vectorstore()

        logger.info(f"DocumentProcessor initialized")
        logger.info(f"  ChromaDB: {chroma_persist_dir}")
        logger.info(f"  Collection: {collection_name}")
        logger.info(f"  Upload directory: {upload_dir}")

    def _load_vectorstore(self) -> None:
        """Load the existing ChromaDB vector store"""
        try:
            persist_path = Path(self.chroma_persist_dir)

            if not persist_path.exists():
                logger.warning(f"ChromaDB directory not found: {persist_path}")
                logger.info("Creating new ChromaDB collection...")
                persist_path.mkdir(parents=True, exist_ok=True)

            self.vectorstore = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=str(persist_path)
            )

            logger.info("Vector store loaded successfully")

        except Exception as e:
            logger.error(f"Failed to load vector store: {e}")
            raise

    def extract_text_from_file(self, file_path: str, file_type: str) -> str:
        """
        Extract text content from uploaded file

        Args:
            file_path: Path to the uploaded file
            file_type: Type of file (txt, md, json, csv, pdf)

        Returns:
            Extracted text content

        Raises:
            ValueError: If file type is not supported
        """
        file_type = file_type.lower().replace('.', '')

        try:
            if file_type in ['txt', 'md']:
                # Plain text and markdown
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()

            elif file_type == 'json':
                # JSON files - convert to readable text
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Pretty print JSON with indentation
                    return json.dumps(data, indent=2)

            elif file_type == 'csv':
                # CSV files - convert to text format
                import csv
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    lines = []
                    for row in reader:
                        # Format each row as key: value pairs
                        row_text = ', '.join([f"{k}: {v}" for k, v in row.items()])
                        lines.append(row_text)
                    return '\n'.join(lines)

            elif file_type == 'pdf':
                # PDF files - extract text using PyPDF2
                try:
                    import PyPDF2
                    with open(file_path, 'rb') as f:
                        pdf_reader = PyPDF2.PdfReader(f)
                        text_parts = []
                        for page_num in range(len(pdf_reader.pages)):
                            page = pdf_reader.pages[page_num]
                            text_parts.append(page.extract_text())
                        return '\n\n'.join(text_parts)
                except ImportError:
                    raise ValueError("PyPDF2 not installed. Install with: pip install PyPDF2")

            else:
                raise ValueError(f"Unsupported file type: {file_type}")

        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {e}")
            raise

    def chunk_document(self, text: str, metadata: Dict) -> List[Document]:
        """
        Split document text into chunks

        Args:
            text: Document text content
            metadata: Metadata to attach to each chunk

        Returns:
            List of Document chunks
        """
        # Create a Document object
        doc = Document(page_content=text, metadata=metadata)

        # Initialize text splitter
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )

        # Split the document
        chunks = splitter.split_documents([doc])

        # Add chunk index to metadata
        for i, chunk in enumerate(chunks):
            chunk.metadata['chunk_index'] = i
            chunk.metadata['total_chunks'] = len(chunks)

        logger.info(f"Created {len(chunks)} chunks from document")
        return chunks

    def add_to_vectorstore(self, chunks: List[Document]) -> int:
        """
        Add document chunks to ChromaDB vector store

        Args:
            chunks: List of Document chunks

        Returns:
            Number of chunks added

        Raises:
            Exception: If failed to add to vector store
        """
        if not chunks:
            logger.warning("No chunks to add to vector store")
            return 0

        try:
            # Add documents to vector store
            self.vectorstore.add_documents(chunks)

            logger.info(f"Successfully added {len(chunks)} chunks to vector store")
            return len(chunks)

        except Exception as e:
            logger.error(f"Failed to add chunks to vector store: {e}")
            raise

    def process_uploaded_file(
        self,
        file_path: str,
        filename: str,
        file_type: str,
        user_id: str,
        company_id: str,
        file_size: int
    ) -> Tuple[int, str]:
        """
        Complete pipeline: Extract, chunk, embed, and store document

        Args:
            file_path: Path to uploaded file
            filename: Original filename
            file_type: File type/extension
            user_id: User who uploaded the file
            company_id: Company ID
            file_size: Size of file in bytes

        Returns:
            Tuple of (number of chunks created, document_id)

        Raises:
            Exception: If processing fails
        """
        logger.info(f"Processing uploaded file: {filename}")

        try:
            # Step 1: Extract text from file
            logger.info("Step 1: Extracting text...")
            text_content = self.extract_text_from_file(file_path, file_type)

            if not text_content or len(text_content.strip()) < 10:
                raise ValueError("File appears to be empty or has insufficient content")

            logger.info(f"Extracted {len(text_content)} characters")

            # Step 2: Create metadata
            document_id = self._generate_document_id(filename, user_id)
            metadata = {
                "source": file_path,
                "filename": filename,
                "file_type": file_type,
                "file_size": file_size,
                "user_id": user_id,
                "company_id": company_id,
                "document_id": document_id,
                "uploaded_at": datetime.utcnow().isoformat(),
                "type": "uploaded_document",
                "category": "user_uploads"
            }

            # Step 3: Chunk the document
            logger.info("Step 2: Chunking document...")
            chunks = self.chunk_document(text_content, metadata)

            # Step 4: Add to vector store
            logger.info("Step 3: Adding to vector store...")
            num_chunks = self.add_to_vectorstore(chunks)

            logger.info(f"✓ Document processed successfully: {num_chunks} chunks created")
            return (num_chunks, document_id)

        except Exception as e:
            logger.error(f"Error processing file {filename}: {e}")
            raise

    def delete_document_from_vectorstore(self, document_id: str) -> bool:
        """
        Delete all chunks of a document from ChromaDB

        Args:
            document_id: Unique document identifier

        Returns:
            True if successful, False otherwise
        """
        try:
            # Get all chunks for this document
            results = self.vectorstore.get(
                where={"document_id": document_id}
            )

            if not results or not results['ids']:
                logger.warning(f"No chunks found for document_id: {document_id}")
                return False

            # Delete all chunks
            self.vectorstore.delete(ids=results['ids'])

            logger.info(f"Deleted {len(results['ids'])} chunks for document {document_id}")
            return True

        except Exception as e:
            logger.error(f"Error deleting document {document_id} from vector store: {e}")
            return False

    def _generate_document_id(self, filename: str, user_id: str) -> str:
        """
        Generate a unique document ID

        Args:
            filename: Original filename
            user_id: User ID

        Returns:
            Unique document ID (UUID string)
        """
        import uuid
        return str(uuid.uuid4())

    def get_vectorstore_stats(self) -> Dict:
        """
        Get statistics about the vector store

        Returns:
            Dictionary with stats
        """
        try:
            collection = self.vectorstore._collection
            count = collection.count()

            return {
                "total_chunks": count,
                "collection_name": self.collection_name,
                "embedding_model": self.embedding_model
            }

        except Exception as e:
            logger.error(f"Error getting vector store stats: {e}")
            return {
                "error": str(e)
            }


# Singleton instance
_document_processor: Optional[DocumentProcessor] = None


def get_document_processor() -> DocumentProcessor:
    """
    Get or create the global DocumentProcessor instance

    Returns:
        DocumentProcessor instance
    """
    global _document_processor

    if _document_processor is None:
        # Get configuration from environment or use defaults
        upload_dir = os.getenv("UPLOAD_DIR", "./uploads")
        chroma_dir = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")

        _document_processor = DocumentProcessor(
            chroma_persist_dir=chroma_dir,
            collection_name="hr_nexus_rag",
            embedding_model="embed-english-v3.0",
            chunk_size=1000,
            chunk_overlap=200,
            upload_dir=upload_dir
        )

    return _document_processor

