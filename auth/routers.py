# auth/routers.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db # Relative import to get_db from parent directory
from models import User  # Absolute import for models
from .schemas import UserResponse, UserCreate, Token  # Absolute import for schemas# from . import service # Will be imported later when you add business logic
from .utils import get_password_hash  # Absolute import for password hashing utilities  

router = APIRouter() # This is your APIRouter instance

# Example: User Registration Endpoint
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter( # Using User directly from models
        (User.email == user.email) | (User.username == user.username)
    ).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )

    hashed_password = get_password_hash(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# Example: Login Endpoint (we'll expand this with verification and JWT soon)
@router.post("/token", response_model=Token)
def login_for_access_token():
    # Authentication logic (e.g., OAuth2, JWT) will go here
    # For now, return dummy token
    return {"access_token": "dummy_token", "token_type": "bearer"}

@router.get("/me/", response_model=UserResponse)
def read_users_me(db: Session = Depends(get_db)):
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user