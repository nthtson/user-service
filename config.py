import os
from datetime import timedelta


class BaseConfig:
    BASE_URL = os.getenv("BASE_URL", "")
    FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL", "")
    SECRET_KEY = os.getenv("SECRET_KEY", "")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "")
    JWT_EXPIRATION_DELTA = timedelta(days=180)

    DATABASE_URL = os.getenv("DATABASE_URL", "")
    TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "")

    MAILTRAP_API_TOKEN = os.getenv("MAILTRAP_API_TOKEN", "")
    MAILTRAP_SENDER_EMAIL = os.getenv("MAILTRAP_SENDER_EMAIL", "")
    MAILTRAP_SENDER_NAME = os.getenv("MAILTRAP_SENDER_EMAIL", "MAILTRAP_SENDER_NAME")
    MAILTRAP_API_URL = os.getenv("MAILTRAP_API_URL", "")

    RABBITMQ_URL = os.getenv("RABBITMQ_URL", "")
    EMAIL_QUEUE_NAME = os.getenv("EMAIL_QUEUE_NAME", "")

    SENTRY_DSN = os.getenv("SENTRY_DSN", "")


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
