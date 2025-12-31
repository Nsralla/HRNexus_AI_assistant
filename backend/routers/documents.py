"""
Document Upload Router for HR Nexus
====================================
Handles document upload, processing, and management endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
from pathlib import Path
import logging

from core.database import get_db
from core.auth import get_current_user
from models.user import User
from models.document import Document as DocumentModel
from services.document_processor import get_document_processor

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/api/documents",
    tags=["documents"]
)

# Allowed file types and max size
ALLOWED_EXTENSIONS = {'.txt', '.md', '.json', '.csv', '.pdf'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def validate_file(file: UploadFile) -> str:
    """
    Validate uploaded file

    Args:
        file: Uploaded file

    Returns:
        File extension

    Raises:
        HTTPException: If file is invalid
    """
    # Check if file has a filename
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No filename provided"
        )

    # Get file extension
    file_ext = Path(file.filename).suffix.lower()

    # Check if extension is allowed
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not supported. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    return file_ext


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload a document and add it to the vector database

    **Process:**
    1. Validate file type and size
    2. Save file to upload directory
    3. Extract text content
    4. Chunk document
    5. Generate embeddings
    6. Store in ChromaDB
    7. Save metadata to PostgreSQL

    **Supported file types:** .txt, .md, .json, .csv, .pdf

    **Max file size:** 10MB
    """
    try:
        # Validate file
        file_ext = validate_file(file)

        # Check file size
        file.file.seek(0, 2)  # Seek to end
        file_size = file.file.tell()
        file.file.seek(0)  # Reset to beginning

        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File size exceeds maximum of 10MB"
            )

        if file_size == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File is empty"
            )

        # Get document processor
        doc_processor = get_document_processor()

        # Create unique filename to avoid collisions
        timestamp = int(os.path.getctime('.') * 1000000)
        safe_filename = f"{timestamp}_{file.filename}"
        file_path = Path(doc_processor.upload_dir) / safe_filename

        # Save uploaded file
        logger.info(f"Saving uploaded file: {file.filename}")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        try:
            # Process the document
            logger.info(f"Processing document: {file.filename}")
            num_chunks, document_id = doc_processor.process_uploaded_file(
                file_path=str(file_path),
                filename=file.filename,
                file_type=file_ext,
                user_id=str(current_user.id),
                company_id=str(current_user.company_id),
                file_size=file_size
            )

            # Save document metadata to database
            import uuid
            db_document = DocumentModel(
                id=uuid.UUID(document_id),  # Convert string to UUID
                company_id=current_user.company_id,
                user_id=current_user.id,
                filename=file.filename,
                file_path=str(file_path),
                file_type=file_ext,
                file_size=file_size
            )
            db.add(db_document)
            db.commit()
            db.refresh(db_document)

            logger.info(f"✓ Document uploaded successfully: {file.filename}")

            return {
                "message": "Document uploaded and processed successfully",
                "file_name": file.filename,
                "file_size": file_size,
                "chunks_created": num_chunks,
                "document_id": document_id
            }

        except Exception as e:
            # Clean up file if processing failed
            if file_path.exists():
                file_path.unlink()
            raise e

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload document: {str(e)}"
        )


@router.get("/")
async def list_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get list of uploaded documents for the current user's company

    Returns list of documents with metadata
    """
    try:
        # Query documents for user's company
        documents = db.query(DocumentModel).filter(
            DocumentModel.company_id == current_user.company_id
        ).order_by(DocumentModel.uploaded_at.desc()).all()

        # Format response
        result = []
        for doc in documents:
            result.append({
                "id": str(doc.id),
                "filename": doc.filename,
                "file_type": doc.file_type,
                "file_size": doc.file_size,
                "uploaded_at": doc.uploaded_at.isoformat(),
                "uploaded_by": str(doc.user_id),
                "status": "completed"  # Could be enhanced to track processing status
            })

        return result

    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve documents"
        )


@router.get("/{document_id}")
async def get_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get details of a specific document
    """
    try:
        # Query document
        document = db.query(DocumentModel).filter(
            DocumentModel.id == document_id,
            DocumentModel.company_id == current_user.company_id
        ).first()

        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )

        return {
            "id": str(document.id),
            "filename": document.filename,
            "file_type": document.file_type,
            "file_size": document.file_size,
            "uploaded_at": document.uploaded_at.isoformat(),
            "uploaded_by": str(document.user_id),
            "file_path": document.file_path,
            "status": "completed"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting document: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve document"
        )


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a document and remove it from the vector database
    """
    try:
        # Query document
        document = db.query(DocumentModel).filter(
            DocumentModel.id == document_id,
            DocumentModel.company_id == current_user.company_id
        ).first()

        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )

        # Delete from vector store
        doc_processor = get_document_processor()
        doc_processor.delete_document_from_vectorstore(document_id)

        # Delete physical file
        file_path = Path(document.file_path)
        if file_path.exists():
            file_path.unlink()
            logger.info(f"Deleted file: {file_path}")

        # Delete from database
        db.delete(document)
        db.commit()

        logger.info(f"✓ Document deleted: {document.filename}")

        return {
            "message": "Document deleted successfully",
            "document_id": document_id
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete document"
        )


@router.get("/stats/vectorstore")
async def get_vectorstore_stats(
    current_user: User = Depends(get_current_user)
):
    """
    Get statistics about the vector store

    **Admin/Debug endpoint**
    """
    try:
        doc_processor = get_document_processor()
        stats = doc_processor.get_vectorstore_stats()

        return stats

    except Exception as e:
        logger.error(f"Error getting vector store stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve statistics"
        )

