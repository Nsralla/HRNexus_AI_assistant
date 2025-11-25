"""
RAG Data Loader Service for HR Nexus
=====================================
This module handles loading and processing data from multiple sources:
1. JSON files from Google Drive (for Colab notebook environment)
2. Markdown files from the local kb/ folder
3. Combines all data into LangChain Documents for RAG processing
4. Creates embeddings and saves to vector database (ChromaDB)

Usage:
    # For Colab Notebook (with Google Drive and vector database):
    loader = RAGDataLoader()
    documents, split_docs, vectorstore = await loader.save_to_vector_database(
        google_drive_url="https://drive.google.com/...",
        download_from_drive=True
    )
    
    # For Local Backend (with persistent vector database):
    loader = RAGDataLoader()
    documents, split_docs, vectorstore = await loader.save_to_vector_database(
        download_from_drive=False,
        persist_directory="./chroma_db"
    )
    
    # Query the vector store:
    results = vectorstore.similarity_search("What is the code review policy?", k=5)
"""

import json
import glob
import os
import re
from typing import List, Optional
from pathlib import Path

# LangChain imports
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Vector database and embeddings imports
try:
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_chroma import Chroma
    import torch
    HAS_VECTOR_DB = True
except ImportError:
    HAS_VECTOR_DB = False
    print("⚠️ Vector database libraries not installed. Install with: pip install langchain-huggingface langchain-chroma torch sentence-transformers")

# Google Drive imports (optional, only for Colab)
try:
    from google.colab import auth
    from googleapiclient.discovery import build
    import gdown
    IS_COLAB = True
except ImportError:
    IS_COLAB = False


class RAGDataLoader:
    """
    Handles loading data from multiple sources for RAG system
    """
    
    def __init__(
        self,
        json_dir: str = "json_files",
        kb_dir: str = "../kb",
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        collection_name: str = "hr_nexus_rag"
    ):
        """
        Initialize the RAG Data Loader
        
        Args:
            json_dir: Directory containing JSON files
            kb_dir: Directory containing markdown knowledge base files
            chunk_size: Size of text chunks for splitting
            chunk_overlap: Overlap between chunks
            embedding_model: HuggingFace model name for embeddings
            collection_name: Name for the ChromaDB collection
        """
        self.json_dir = json_dir
        self.kb_dir = kb_dir
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embedding_model = embedding_model
        self.collection_name = collection_name
        
        # Get absolute paths
        self.base_dir = Path(__file__).parent.parent
        self.json_path = self.base_dir / json_dir
        self.kb_path = self.base_dir / kb_dir
        
        # Initialize embedding and vector store (will be set when create_vector_store is called)
        self.embeddings = None
        self.vectorstore = None
        
    async def download_from_google_drive(
        self,
        folder_url: str,
        output_dir: Optional[str] = None
    ) -> List[str]:
        """
        Download JSON files from Google Drive folder (Colab only)
        
        Args:
            folder_url: Google Drive folder URL
            output_dir: Output directory (defaults to self.json_dir)
            
        Returns:
            List of downloaded file paths
        """
        if not IS_COLAB:
            print("⚠️ Not in Colab environment - skipping Google Drive download")
            return []
            
        output_dir = output_dir or self.json_dir
        
        # Extract folder ID from URL
        match = re.search(r"folders/([a-zA-Z0-9_-]+)", folder_url)
        if not match:
            raise ValueError("Invalid Google Drive folder URL")
        
        folder_id = match.group(1)
        print(f"📁 Google Drive Folder ID: {folder_id}")
        
        # Authenticate user
        auth.authenticate_user()
        
        # Build Drive service
        drive_service = build('drive', 'v3')
        
        # List JSON files in the folder
        results = drive_service.files().list(
            q=f"'{folder_id}' in parents and mimeType='application/json'",
            fields="files(id, name)"
        ).execute()
        
        files = results.get('files', [])
        print(f"📊 Found {len(files)} JSON files in Google Drive")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Download each file
        downloaded_files = []
        for file in files:
            file_id = file['id']
            file_name = file['name']
            output_path = f"{output_dir}/{file_name}"
            
            gdown.download(
                f"https://drive.google.com/uc?id={file_id}",
                output_path,
                quiet=False
            )
            downloaded_files.append(output_path)
        
        print(f"✅ Downloaded {len(downloaded_files)} JSON files")
        return downloaded_files
    
    def load_json_files(self, json_dir: Optional[str] = None) -> List[Document]:
        """
        Load JSON files and convert to LangChain Documents
        
        Args:
            json_dir: Directory containing JSON files (defaults to self.json_dir)
            
        Returns:
            List of Document objects
        """
        json_dir = json_dir or self.json_path
        documents = []
        
        # Support both string path and Path object
        if isinstance(json_dir, str):
            json_dir = Path(json_dir)
            
        # Find all JSON files
        json_files = list(json_dir.glob("*.json"))
        
        if not json_files:
            print(f"⚠️ No JSON files found in {json_dir}")
            return documents
        
        for file_path in json_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    
                    # Convert JSON to formatted string
                    content = json.dumps(data, indent=2)
                    
                    # Create Document with metadata
                    doc = Document(
                        page_content=content,
                        metadata={
                            "source": str(file_path),
                            "type": "json",
                            "filename": file_path.name,
                            "category": self._get_category_from_filename(file_path.name)
                        }
                    )
                    documents.append(doc)
                    
            except Exception as e:
                print(f"❌ Error loading {file_path}: {e}")
        
        print(f"✅ Loaded {len(documents)} JSON documents")
        return documents
    
    def load_markdown_files(self, kb_dir: Optional[str] = None) -> List[Document]:
        """
        Load Markdown files from knowledge base directory
        
        Args:
            kb_dir: Directory containing markdown files (defaults to self.kb_dir)
            
        Returns:
            List of Document objects
        """
        kb_dir = kb_dir or self.kb_path
        documents = []
        
        # Support both string path and Path object
        if isinstance(kb_dir, str):
            kb_dir = Path(kb_dir)
        
        # Find all markdown files
        md_files = list(kb_dir.glob("*.md"))
        
        if not md_files:
            print(f"⚠️ No markdown files found in {kb_dir}")
            return documents
        
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
                    
            except Exception as e:
                print(f"❌ Error loading {file_path}: {e}")
        
        print(f"✅ Loaded {len(documents)} markdown documents")
        return documents
    
    async def load_all_documents(
        self,
        google_drive_url: Optional[str] = None,
        download_from_drive: bool = False
    ) -> List[Document]:
        """
        Load all documents from both JSON and Markdown sources
        
        Args:
            google_drive_url: Google Drive folder URL (optional)
            download_from_drive: Whether to download from Google Drive first
            
        Returns:
            List of all Document objects combined
        """
        print("\n" + "="*80)
        print("📚 LOADING DATA FROM MULTIPLE SOURCES")
        print("="*80 + "\n")
        
        all_documents = []
        
        # Step 1: Download from Google Drive if requested
        if download_from_drive and google_drive_url and IS_COLAB:
            print("🔽 Step 1: Downloading JSON files from Google Drive...")
            await self.download_from_google_drive(google_drive_url)
            print()
        
        # Step 2: Load JSON files
        print("📄 Step 2: Loading JSON files...")
        json_docs = self.load_json_files()
        all_documents.extend(json_docs)
        print()
        
        # Step 3: Load Markdown files from kb folder
        print("📝 Step 3: Loading Markdown files from kb folder...")
        md_docs = self.load_markdown_files()
        all_documents.extend(md_docs)
        print()
        
        # Summary
        print("="*80)
        print(f"✅ TOTAL DOCUMENTS LOADED: {len(all_documents)}")
        print(f"   - JSON files: {len(json_docs)}")
        print(f"   - Markdown files: {len(md_docs)}")
        print("="*80 + "\n")
        
        return all_documents
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into smaller chunks for better retrieval
        
        Args:
            documents: List of Document objects to split
            
        Returns:
            List of split Document objects
        """
        if not documents:
            print("⚠️ No documents to split")
            return []
        
        print(f"✂️ Splitting {len(documents)} documents...")
        print(f"   Chunk size: {self.chunk_size}, Overlap: {self.chunk_overlap}")
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
        
        split_docs = splitter.split_documents(documents)
        
        print(f"✅ Created {len(split_docs)} chunks from {len(documents)} documents")
        return split_docs
    
    def _get_category_from_filename(self, filename: str) -> str:
        """Extract category from JSON filename (e.g., 'projects.json' -> 'projects')"""
        return filename.replace('.json', '').replace('_', ' ').title()
    
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
            "json_documents": sum(1 for d in documents if d.metadata.get("type") == "json"),
            "markdown_documents": sum(1 for d in documents if d.metadata.get("type") == "markdown"),
            "total_characters": sum(len(d.page_content) for d in documents),
            "categories": {}
        }
        
        # Count by category
        for doc in documents:
            category = doc.metadata.get("category", "unknown")
            stats["categories"][category] = stats["categories"].get(category, 0) + 1
        
        return stats
    
    def initialize_embeddings(self):
        """
        Initialize the HuggingFace embeddings model
        
        Returns:
            HuggingFaceEmbeddings instance
        """
        if not HAS_VECTOR_DB:
            raise ImportError(
                "Vector database libraries not installed. "
                "Install with: pip install langchain-huggingface langchain-chroma torch sentence-transformers"
            )
        
        print(f"🔧 Initializing embeddings model: {self.embedding_model}")
        
        try:
            import torch
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
            print(f"   Running on: {device.upper()}")
        except:
            device = 'cpu'
        
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.embedding_model,
            model_kwargs={'device': device},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        print("✅ Embeddings model initialized")
        return self.embeddings
    
    def create_vector_store(self, documents: List[Document], persist_directory: Optional[str] = None):
        """
        Create a vector store from documents with embeddings
        
        Args:
            documents: List of Document objects (should be split chunks)
            persist_directory: Optional directory to persist the vector store
            
        Returns:
            Chroma vector store instance
        """
        if not HAS_VECTOR_DB:
            raise ImportError(
                "Vector database libraries not installed. "
                "Install with: pip install langchain-huggingface langchain-chroma torch sentence-transformers"
            )
        
        if not documents:
            print("⚠️ No documents to create vector store")
            return None
        
        # Initialize embeddings if not already done
        if self.embeddings is None:
            self.initialize_embeddings()
        
        print(f"\n{'='*80}")
        print(f"🗄️ CREATING VECTOR STORE")
        print(f"{'='*80}\n")
        print(f"📊 Processing {len(documents)} document chunks...")
        
        # Count document types
        json_count = sum(1 for d in documents if d.metadata.get('type') == 'json')
        md_count = sum(1 for d in documents if d.metadata.get('type') == 'markdown')
        
        print(f"   - JSON chunks: {json_count}")
        print(f"   - Markdown chunks: {md_count}")
        
        # Create vector store
        if persist_directory:
            self.vectorstore = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                collection_name=self.collection_name,
                persist_directory=persist_directory
            )
            print(f"\n✅ Vector store created and persisted to: {persist_directory}")
        else:
            self.vectorstore = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                collection_name=self.collection_name
            )
            print(f"\n✅ Vector store created (in-memory)")
        
        print(f"   Collection name: {self.collection_name}")
        print(f"   Total chunks: {len(documents)}")
        print(f"{'='*80}\n")
        
        return self.vectorstore
    
    async def save_to_vector_database(
        self,
        google_drive_url: Optional[str] = None,
        download_from_drive: bool = False,
        persist_directory: Optional[str] = None
    ):
        """
        Complete pipeline: Load documents, create embeddings, and save to vector database
        
        Args:
            google_drive_url: Google Drive folder URL (optional)
            download_from_drive: Whether to download from Google Drive first
            persist_directory: Optional directory to persist the vector store
            
        Returns:
            Tuple of (documents, split_docs, vectorstore)
        """
        print("\n" + "="*80)
        print("🚀 RAG DATA LOADER - COMPLETE PIPELINE")
        print("="*80 + "\n")
        
        # Step 1: Load all documents
        documents = await self.load_all_documents(
            google_drive_url=google_drive_url,
            download_from_drive=download_from_drive
        )
        
        if not documents:
            print("⚠️ No documents loaded. Aborting.")
            return ([], [], None)
        
        # Step 2: Split documents
        split_docs = self.split_documents(documents)
        
        # Step 3: Create vector store with embeddings
        vectorstore = self.create_vector_store(split_docs, persist_directory=persist_directory)
        
        # Final summary
        print("="*80)
        print("✅ PIPELINE COMPLETE!")
        print("="*80)
        print(f"📚 Documents loaded: {len(documents)}")
        print(f"✂️ Chunks created: {len(split_docs)}")
        print(f"🗄️ Vector store: {'Ready' if vectorstore else 'Failed'}")
        print("="*80 + "\n")
        
        return (documents, split_docs, vectorstore)


# Example usage for Colab Notebook
async def main_colab():
    """
    Example usage in Google Colab notebook with vector database
    """
    # Configuration
    GOOGLE_DRIVE_URL = "https://drive.google.com/drive/folders/1QzHjx32cNZgruG7rznmtf9DnVF4IzauO?usp=share_link"
    
    # Initialize loader
    loader = RAGDataLoader(
        json_dir="json_files",
        kb_dir="../kb",
        chunk_size=500,
        chunk_overlap=50,
        embedding_model="sentence-transformers/all-MiniLM-L6-v2",
        collection_name="hr_nexus_rag"
    )
    
    # Run complete pipeline: load documents, create embeddings, save to vector DB
    documents, split_docs, vectorstore = await loader.save_to_vector_database(
        google_drive_url=GOOGLE_DRIVE_URL,
        download_from_drive=True,
        persist_directory=None  # In-memory for Colab
    )
    
    # Get statistics
    stats = loader.get_statistics(split_docs)
    print("\n📊 Statistics:")
    print(json.dumps(stats, indent=2))
    
    # Test vector store with a query
    if vectorstore:
        print("\n🔍 Testing vector store with sample query...")
        results = vectorstore.similarity_search("What projects are in progress?", k=3)
        print(f"✅ Retrieved {len(results)} relevant documents")
    
    return vectorstore


# Example usage for Local Backend
async def main_backend():
    """
    Example usage in local backend environment with persistent vector database
    """
    # Initialize loader with backend paths
    loader = RAGDataLoader(
        json_dir="sources",  # Use local sources directory
        kb_dir="../kb",
        chunk_size=500,
        chunk_overlap=50,
        embedding_model="sentence-transformers/all-MiniLM-L6-v2",
        collection_name="hr_nexus_rag"
    )
    
    # Run complete pipeline with persistent storage
    documents, split_docs, vectorstore = await loader.save_to_vector_database(
        download_from_drive=False,
        persist_directory="./chroma_db"  # Persist to local directory
    )
    
    # Get statistics
    stats = loader.get_statistics(split_docs)
    print("\n📊 Statistics:")
    print(json.dumps(stats, indent=2))
    
    # Test vector store with a query
    if vectorstore:
        print("\n🔍 Testing vector store with sample query...")
        results = vectorstore.similarity_search("What is the team structure?", k=3)
        print(f"✅ Retrieved {len(results)} relevant documents")
        for i, doc in enumerate(results, 1):
            print(f"\n  [{i}] {doc.metadata.get('filename')} ({doc.metadata.get('type')})")
            print(f"      {doc.page_content[:100]}...")
    
    return vectorstore


if __name__ == "__main__":
    import asyncio
    
    # Run backend version
    asyncio.run(main_backend())
