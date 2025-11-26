from fastapi import APIRouter, status, Depends, HTTPException
from schemas.message import MessageCreate, MessageResponse
from schemas.chat import ChatCreate, ChatUpdate, ChatResponse
from sqlalchemy.orm import Session
from core.database import get_db
from core.auth import get_current_user
from models.user import User
from models.chat import Chat
from models.message import Message
from uuid import UUID
from services.chat_pipeline import chat_pipe

router = APIRouter(prefix="/api/chat", tags=["Chat"])


@router.post("/", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
async def create_chat(
    chat_data: ChatCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        """Create a new chat conversation"""
        new_chat = Chat(
            user_id=current_user.id,
            company_id=current_user.company_id,
            title=chat_data.title
        )
        db.add(new_chat)
        db.commit()
        db.refresh(new_chat)
        return new_chat
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

   


@router.get("/", response_model=list[ChatResponse])
async def get_user_chats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all chats for the current user"""
    chats = db.query(Chat).filter(Chat.user_id == current_user.id).order_by(Chat.created_at.desc()).all()
    return chats


@router.patch("/{chat_id}", response_model=ChatResponse)
async def update_chat(
    chat_id: str,
    chat_data: ChatUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update chat title"""
    try:
        # Validate UUID
        chat_uuid = UUID(chat_id)

        # Verify chat exists and belongs to current user
        chat = db.query(Chat).filter(Chat.id == chat_uuid).first()
        if not chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat not found"
            )

        if chat.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to update this chat"
            )

        # Update chat title
        chat.title = chat_data.title
        db.commit()
        db.refresh(chat)

        return chat
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid chat ID"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(
    chat_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a chat and all its messages"""
    try:
        # Validate UUID
        chat_uuid = UUID(chat_id)

        # Verify chat exists and belongs to current user
        chat = db.query(Chat).filter(Chat.id == chat_uuid).first()
        if not chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat not found"
            )

        if chat.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to delete this chat"
            )

        # Delete all messages associated with the chat
        db.query(Message).filter(Message.chat_id == chat_uuid).delete()

        # Delete the chat
        db.delete(chat)
        db.commit()

        return None
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid chat ID"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/message", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_message(
    message_data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Receive a new message and save it to the database"""

    if not message_data.content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message content is required"
        )

    # Verify chat exists and belongs to current user
    chat = db.query(Chat).filter(Chat.id == message_data.chat_id).first()
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )

    if chat.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this chat"
        )

    # Create user message
    user_message = Message(
        chat_id=message_data.chat_id,
        user_id=current_user.id,
        content=message_data.content,
        role="user"
    )
    db.add(user_message)
    db.commit()
    db.refresh(user_message)

    # Get chat history for context
    previous_messages = db.query(Message).filter(
        Message.chat_id == message_data.chat_id
    ).order_by(Message.created_at.asc()).all()

    # Convert to chat history format (list of dicts with role and content)
    chat_history = [
        {"role": msg.role, "content": msg.content}
        for msg in previous_messages
    ]

    # Send to LangGraph pipeline with chat history
    response = await chat_pipe.run(message_data.content, chat_history)

    # Create assistant response
    assistant_response = Message(
        chat_id=message_data.chat_id,
        user_id=current_user.id,
        content=response,
        role="assistant"
    )
    db.add(assistant_response)
    db.commit()
    db.refresh(assistant_response)

    return assistant_response


@router.get("/{chat_id}/messages", response_model=list[MessageResponse])
async def get_chat_messages(
    chat_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all messages for a specific chat"""
    
    try:
        # validate it's uuid
        if not chat_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Chat ID is required"
            )
        
        chat_uuid = UUID(chat_id)
        if not chat_uuid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid chat ID"
            )
        
        # Verify chat exists and belongs to current user
        chat = db.query(Chat).filter(Chat.id == chat_id).first()
        if not chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat not found"
            )

        if chat.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to access this chat"
            )

        messages = db.query(Message).filter(Message.chat_id == chat_id).order_by(Message.created_at.asc()).all()
        return messages
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
