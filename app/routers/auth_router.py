from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from jose import jwt

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from dotenv import load_dotenv

import os

from app.database import get_db

from app.models.user import User

from app.schemas.user_schema import UserCreate

from app.schemas.auth_schema import LoginSchema

from app.utils.password_handler import (
    hash_password,
    verify_password
)

from app.utils.jwt_handler import (
    create_access_token
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

security = HTTPBearer()

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = os.getenv("ALGORITHM")


@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(
            user.password
        ),
        role=user.role
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {
        "message": "User registered successfully"
    }


@router.post("/login")
def login(
    data: LoginSchema,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == data.email
    ).first()

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email"
        )

    if not verify_password(
        data.password,
        user.hashed_password
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    token = create_access_token(
        {
            "user_id": user.id,
            "role": user.role
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/me")
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    return {
        "user_id": payload["user_id"],
        "role": payload["role"]
    }