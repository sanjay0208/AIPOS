from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth.schemas import UserRegister
from app.auth.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.database.models.user import User


def register_user(db: Session, user: UserRegister) -> User:
    """
    Register a new user.
    """

    # Check if email already exists
    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    hashed_password = hash_password(user.password)

    db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def login_user(
    db: Session,
    email: str,
    password: str,
):
    """
    Authenticate user and return JWT token.
    """

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    print("\n========== LOGIN DEBUG ==========")
    print("Email:", email)
    print("Entered Password:", password)
    print("Stored Hash:", user.hashed_password)

    is_valid = verify_password(
        password,
        user.hashed_password,
    )

    print("Password Valid:", is_valid)
    print("================================\n")

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(
        {"sub": user.email}
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }