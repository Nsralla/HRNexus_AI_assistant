from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import uuid

from core.database import get_db
from core.auth import hash_password, verify_password, create_access_token, get_current_user
from schemas.user import UserCreate, UserLogin, UserResponse, Token, OAuth2Token
from models import User, Company

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    
    # Check if company_id provided, otherwise create new company
    if user_data.company_id:
        company = db.query(Company).filter(Company.id == user_data.company_id).first()
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company not found"
            )
        company_id = company.id
    else:
        # Create new company (use first part of email as company name)
        company_name = user_data.email.split('@')[1].split('.')[0].capitalize()
        new_company = Company(name=f"{company_name} Company")
        db.add(new_company)
        db.flush()
        company_id = new_company.id
    
    # Check if user already exists
    existing_user = db.query(User).filter(
        User.company_id == company_id,
        User.email == user_data.email
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered for this company"
        )
    
    # Create new user
    hashed_pw = hash_password(user_data.password)
    new_user = User(
        company_id=company_id,
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_pw,
        role="admin" if not user_data.company_id else "employee"  # First user is admin
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


@router.post("/login", response_model=OAuth2Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login user (OAuth2 compatible for Swagger UI)"""

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


@router.post("/login/json", response_model=Token)
async def login_json(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user with JSON body (alternative endpoint)"""

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


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user info"""
    return UserResponse.from_orm(current_user)
