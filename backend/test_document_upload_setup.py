"""
Test Script for Document Upload System
=======================================
Quick verification that all components are set up correctly.
"""
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 80)
print("DOCUMENT UPLOAD SYSTEM - SETUP VERIFICATION")
print("=" * 80)

# Check 1: Import dependencies
print("\n[1] Checking dependencies...")
try:
    from services.document_processor import DocumentProcessor, get_document_processor
    print("✓ Document processor imports successful")
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)

try:
    from routers.documents import router
    print("✓ Document router imports successful")
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)

try:
    from langchain_cohere import CohereEmbeddings
    from langchain_chroma import Chroma
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    print("✓ LangChain dependencies available")
except ImportError as e:
    print(f"✗ LangChain import error: {e}")
    sys.exit(1)

# Check 2: Environment variables
print("\n[2] Checking environment variables...")
cohere_key = os.getenv("COHERE_API_KEY")
if cohere_key:
    print(f"✓ COHERE_API_KEY is set (length: {len(cohere_key)})")
else:
    print("⚠ COHERE_API_KEY not set - embeddings will fail")

# Check 3: Directory structure
print("\n[3] Checking directories...")
upload_dir = Path("./uploads")
if upload_dir.exists():
    print(f"✓ Upload directory exists: {upload_dir.absolute()}")
else:
    print(f"✗ Upload directory missing: {upload_dir.absolute()}")
    print("  Creating...")
    upload_dir.mkdir(parents=True, exist_ok=True)
    print("✓ Upload directory created")

chroma_dir = Path("./chroma_db")
if chroma_dir.exists():
    print(f"✓ ChromaDB directory exists: {chroma_dir.absolute()}")
else:
    print(f"⚠ ChromaDB directory not found: {chroma_dir.absolute()}")
    print("  It will be created on first upload")

# Check 4: Test document processor initialization
print("\n[4] Testing document processor...")
try:
    processor = DocumentProcessor(
        chroma_persist_dir="./chroma_db",
        collection_name="hr_nexus_rag_test",
        embedding_model="embed-english-v3.0",
        upload_dir="./uploads"
    )
    print("✓ Document processor initialized")
    
    # Test stats
    stats = processor.get_vectorstore_stats()
    print(f"✓ Vector store stats: {stats}")
    
except Exception as e:
    print(f"✗ Error initializing processor: {e}")
    print(f"  Type: {type(e).__name__}")

# Check 5: Test text extraction
print("\n[5] Testing text extraction...")
test_file = Path("./uploads/test_document.txt")
try:
    # Create test file
    test_content = "This is a test document for the HR Nexus upload system. It contains sample text."
    test_file.write_text(test_content)
    print(f"✓ Created test file: {test_file}")
    
    # Test extraction
    extracted = processor.extract_text_from_file(str(test_file), "txt")
    if extracted == test_content:
        print("✓ Text extraction working correctly")
    else:
        print("✗ Text extraction mismatch")
    
    # Cleanup
    test_file.unlink()
    print("✓ Test file cleaned up")
    
except Exception as e:
    print(f"✗ Error in text extraction: {e}")
    if test_file.exists():
        test_file.unlink()

# Check 6: Test chunking
print("\n[6] Testing document chunking...")
try:
    test_text = "This is a test. " * 100  # Create longer text
    metadata = {
        "filename": "test.txt",
        "user_id": "test-user",
        "company_id": "test-company"
    }
    
    chunks = processor.chunk_document(test_text, metadata)
    print(f"✓ Created {len(chunks)} chunks from test text")
    
    if chunks:
        first_chunk = chunks[0]
        print(f"  Chunk metadata keys: {list(first_chunk.metadata.keys())}")
        
except Exception as e:
    print(f"✗ Error in chunking: {e}")

# Check 7: Test router
print("\n[7] Checking router setup...")
try:
    from routers.documents import router, ALLOWED_EXTENSIONS, MAX_FILE_SIZE
    print(f"✓ Router configured")
    print(f"  Allowed extensions: {ALLOWED_EXTENSIONS}")
    print(f"  Max file size: {MAX_FILE_SIZE / (1024*1024):.1f} MB")
    print(f"  Endpoints: {len(router.routes)} routes")
    
except Exception as e:
    print(f"✗ Error checking router: {e}")

# Summary
print("\n" + "=" * 80)
print("VERIFICATION COMPLETE")
print("=" * 80)

if cohere_key:
    print("\n✅ System is ready for document uploads!")
    print("\nNext steps:")
    print("1. Start the backend: python3 -m uvicorn main:app --reload")
    print("2. Use the frontend to upload documents")
    print("3. Documents will be automatically embedded and searchable")
else:
    print("\n⚠ System setup complete but COHERE_API_KEY is missing")
    print("\nTo enable uploads:")
    print("1. Set COHERE_API_KEY environment variable")
    print("2. Restart the backend server")

print("\n" + "=" * 80)

