from sqlalchemy.orm import Session

from app.auth.security import hash_password
from app.database.models.user import User
from app.auth.schemas import UserRegister


def register_user(db: Session, user: UserRegister) -> User:
    """
    Register a new user.
    """

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