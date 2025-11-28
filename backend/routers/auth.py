from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError, DBAPIError
import uuid
import logging

from core.database import get_db
from core.auth import hash_password, verify_password, create_access_token, get_current_user
from schemas.user import UserCreate, UserLogin, UserResponse, Token, OAuth2Token
from models import User, Company

# Setup logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user with comprehensive validation"""

    try:
        # Validate password strength (minimum 8 characters)
        if len(user_data.password) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 8 characters long"
            )

        # Validate full_name is not empty
        if not user_data.full_name or not user_data.full_name.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Full name is required"
            )

        # Validate that company_id is provided and exists
        if not user_data.company_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Company ID is required. Please use the default company ID or contact your administrator."
            )

        company = db.query(Company).filter(Company.id == user_data.company_id).first()
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company not found. Please check your company ID or use the default one."
            )
        company_id = company.id

        # Check if user already exists for this company
        existing_user = db.query(User).filter(
            User.company_id == company_id,
            User.email == user_data.email
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered for this company"
            )

        # Create new user with hashed password
        hashed_pw = hash_password(user_data.password)
        new_user = User(
            company_id=company_id,
            name=user_data.full_name.strip(),
            email=user_data.email.lower(),
            hashed_password=hashed_pw,
            role="employee"  # All new signups start as employee
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # Create access token
        access_token = create_access_token(data={"sub": str(new_user.id)})

        return Token(
            access_token=access_token,
            user=UserResponse.from_orm(new_user)
        )

    except HTTPException:
        # Re-raise HTTP exceptions (validation errors, etc.)
        raise

    except (OperationalError, DBAPIError) as e:
        # Database connection errors
        db.rollback()
        logger.error(f"Database connection error during registration: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Our service is temporarily unavailable. Please try again in a moment."
        )

    except Exception as e:
        # Catch any other unexpected errors
        db.rollback()
        logger.error(f"Unexpected error during registration: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user. Please try again later."
        )


@router.post("/login", response_model=OAuth2Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login user (OAuth2 compatible for Swagger UI)"""

    try:
        # Find user by email (username field in OAuth2 form contains email)
        user = db.query(User).filter(User.email == form_data.username).first()

        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create access token
        access_token = create_access_token(data={"sub": str(user.id)})

        return OAuth2Token(
            access_token=access_token,
            token_type="bearer"
        )

    except HTTPException:
        raise

    except (OperationalError, DBAPIError) as e:
        logger.error(f"Database connection error during login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Our service is temporarily unavailable. Please try again in a moment."
        )

    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later."
        )


@router.post("/login/json", response_model=Token)
async def login_json(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user with JSON body (alternative endpoint)"""

    try:
        # Find user by email
        user = db.query(User).filter(User.email == credentials.email).first()

        if not user or not verify_password(credentials.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create access token
        access_token = create_access_token(data={"sub": str(user.id)})

        return Token(
            access_token=access_token,
            user=UserResponse.from_orm(user)
        )

    except HTTPException:
        # Re-raise HTTP exceptions (like 401 Unauthorized)
        raise

    except (OperationalError, DBAPIError) as e:
        # Database connection errors
        logger.error(f"Database connection error during login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Our service is temporarily unavailable. Please try again in a moment."
        )

    except Exception as e:
        # Catch any other unexpected errors
        logger.error(f"Unexpected error during login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later."
        )


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user info"""
    return UserResponse.from_orm(current_user)
