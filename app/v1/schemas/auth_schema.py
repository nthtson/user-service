from dataclasses import dataclass


@dataclass
class RegisterRequest:
    email: str
    password: str
    first_name: str
    last_name: str
    phone_number: str


@dataclass
class LoginRequest:
    email: str
    password: str


@dataclass
class AuthResponse:
    access_token: str
    token_type: str = "bearer"


@dataclass
class RequestPasswordResetRequest:
    email: str


@dataclass
class ResetPasswordRequest:
    token: str
    new_password: str
