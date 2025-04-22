from datetime import datetime, timedelta
from typing import Any, Mapping, Optional

import pytz
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.scoping import scoped_session

from app.core.error_handlers import NotFoundException, ValidationException
from app.v1.models.user import User
from app.v1.schemas.auth_schema import RegisterRequest


class UserRepository:
    def __init__(self, session: scoped_session):
        self.session = session

    def create_user(self, req_data: RegisterRequest, verification_token: str) -> User:
        try:
            new_user = User()
            new_user.email = req_data.email
            new_user.password_hash = req_data.password
            new_user.first_name = req_data.first_name
            new_user.last_name = req_data.last_name
            new_user.phone_number = req_data.phone_number
            new_user.is_email_verified = False
            new_user.verification_token = verification_token
            new_user.verification_token_expiry = datetime.now(tz=pytz.utc) + timedelta(
                hours=1
            )  # Expires in 1 hour
            self.session.add(new_user)
            self.session.commit()
            return new_user
        except SQLAlchemyError as e:
            self.session.rollback()
            raise Exception(f"Error creating user: {str(e)}")

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.session.query(User).filter_by(email=email).first()

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.session.query(User).filter_by(id=user_id).first()

    def verify_email(self, verification_token: str) -> None:
        try:
            user: Optional[User] = (
                self.session.query(User)
                .filter_by(verification_token=verification_token)
                .first()
            )
            if not user:
                raise NotFoundException("Invalid or expired token")

            if (
                user.verification_token_expiry
                and user.verification_token_expiry < datetime.now(tz=pytz.utc)
            ):
                raise ValidationException("Token has expired")

            user.is_email_verified = True
            user.verification_token = None
            user.verification_token_expiry = None
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise Exception(f"Error verifying email: {str(e)}")

    def update_user(self, user_id: int, **kwargs: Mapping[str, Any]) -> Optional[User]:
        user: Optional[User] = (
            self.session.query(User).filter(User.id == user_id).first()
        )
        if not user:
            return None
        for key, value in kwargs.items():
            setattr(user, key, value)
        self.session.commit()
        self.session.refresh(user)
        return user
