# auth/routers.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm # For FastAPI's login form handling
from sqlalchemy.orm import Session
from datetime import timedelta # Add this import
import os

# Import your database, models, schemas, utils, and NEW service.py
from database import get_db
from models import User # Only User is directly needed here now
from .schemas import UserCreate, UserResponse, Token, UserLogin # Add UserLogin and Token
from .utils import get_password_hash, verify_password # Add verify_password
from .service import authenticate_user, create_access_token, get_current_user # NEW imports

router = APIRouter()

# User Registration Endpoint (remains mostly the same)
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(
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

# --- Login Endpoint (Now implements actual authentication and JWT generation) ---
@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), # FastAPI utility for login forms
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Access token expires after a configurable time
    access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# --- Protected Endpoint (requires a valid JWT to access) ---
# The `get_current_user` dependency ensures the user is authenticated and active
@router.get("/me/", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)): # Use the dependency!
    return current_user