import secrets
from typing import Optional

from flask_jwt_extended import create_access_token
from sqlalchemy.orm.scoping import scoped_session
from werkzeug.security import check_password_hash, generate_password_hash

from app.core.error_handlers import (
    ErrorVerifyingEmailException,
    ValidationException,
)
from app.v1.events.email_publisher import EmailPublisher
from app.v1.models import User
from app.v1.repositories.user_repository import UserRepository
from app.v1.schemas.auth_schema import (
    AuthResponse,
    LoginRequest,
    RegisterRequest,
)
from app.v1.schemas.email_schema import EmailMessage


class AuthService:
    def __init__(
        self, session: scoped_session, rabbitmq_url: str, frontend_base_url: str
    ):
        self.user_repo = UserRepository(session)
        self.rabbitmq_url = rabbitmq_url
        self.frontend_base_url = frontend_base_url

    def register_user(self, req_data: RegisterRequest) -> None:
        existing_user = self.user_repo.get_user_by_email(req_data.email)
        if existing_user:
            raise ValidationException("User already exists")

        # Hash the password before storing it
        hashed_password = generate_password_hash(req_data.password)
        verification_token = secrets.token_urlsafe(32)
        try:
            req_data.password = hashed_password
            user: Optional[User] = self.user_repo.create_user(
                req_data, verification_token
            )
            if not user:
                raise ValueError("Something went wrong")

            self.send_verification_email(
                email=user.email, full_name=user.full_name, token=verification_token
            )

        except Exception as e:
            raise Exception(f"Error registering user: {str(e)}")

    def authenticate_user(self, req_data: LoginRequest) -> AuthResponse:
        user: Optional[User] = self.user_repo.get_user_by_email(req_data.email)
        if (
            not user
            or not check_password_hash(user.password_hash, req_data.password)
            or (user and not user.is_email_verified)
        ):
            raise ValueError("Invalid credentials")

        # Generate JWT token
        token = create_access_token(
            identity=str(user.id), additional_claims={"email": user.email}
        )
        return AuthResponse(access_token=token)

    def verify_email(self, token: str) -> None:
        try:
            self.user_repo.verify_email(token)
        except Exception as e:
            raise ErrorVerifyingEmailException(f"Error verifying email: {str(e)}")

    def send_verification_email(self, email: str, full_name: str, token: str) -> None:
        link = f"{self.frontend_base_url}/v1/users/verify-email?token={token}"
        subject = "Verify your account"
        body = f"Click the link to verify: {link}"
        publisher = EmailPublisher(self.rabbitmq_url)
        publisher.publish_email(
            EmailMessage(
                to_email=email, full_name=full_name, subject=subject, body=body
            )
        )
