from datetime import datetime
from typing import Any, Dict, Optional

from passlib.hash import bcrypt
from sqlalchemy.orm import Mapped

from app.db.database import db
from app.v1.models import Base


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = db.Column(db.String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = db.Column(db.String(255), nullable=False)

    first_name: Mapped[str] = db.Column(db.String(100), nullable=False)
    last_name: Mapped[str] = db.Column(db.String(100), nullable=False)
    phone_number: Mapped[str] = db.Column(db.String(30), nullable=False)
    is_active: Mapped[bool] = db.Column(db.Boolean, default=True, nullable=False)
    is_admin: Mapped[bool] = db.Column(db.Boolean, default=False, nullable=False)

    is_email_verified: Mapped[bool] = db.Column(
        db.Boolean, default=False, nullable=False
    )
    verification_token: Mapped[Optional[str]] = db.Column(db.String(128), nullable=True)
    verification_token_expiry: Mapped[Optional[datetime]] = db.Column(
        db.DateTime(timezone=True), nullable=True
    )

    def set_password(self, password: str) -> None:
        self.password_hash = bcrypt.hash(password)

    def check_password(self, password: str) -> bool:
        return bcrypt.verify(password, self.password_hash)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
        }
