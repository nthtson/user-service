from datetime import datetime, timedelta

import jwt
import pytest
import pytz
from flask.testing import FlaskClient
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app import create_app
from app.v1 import models
from app.v1.models import User
from config import BaseConfig


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(BaseConfig.TEST_DATABASE_URL)
    models.Base.metadata.create_all(engine)  # 👈 Ensure all tables are created
    yield engine
    models.Base.metadata.drop_all(engine)  # Optional cleanup


@pytest.fixture(scope="function")
def db_session(db_engine):
    # Use sessionmaker to create a new session factory
    session = scoped_session(
        sessionmaker(bind=db_engine, autocommit=False, autoflush=False)
    )
    yield session
    session.rollback()
    session.close()


@pytest.fixture(scope="module")
def app():
    app = create_app(BaseConfig.TEST_DATABASE_URL, testing=True)
    yield app


@pytest.fixture(scope="module")
def client(app) -> FlaskClient:
    return app.test_client()


@pytest.fixture
def test_user(db_session):
    user = User()
    user.email = "test_user@example.com"
    user.first_name = "first_name"
    user.last_name = "last_name"
    user.phone_number = "+8412345678"
    user.password_hash = "fakehashedpassword"

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


@pytest.fixture
def auth_token(test_user):
    payload = {
        "sub": str(test_user.id),
        "exp": datetime.now(tz=pytz.utc) + timedelta(hours=1),
    }
    token = jwt.encode(payload, BaseConfig.JWT_SECRET_KEY, algorithm="HS256")
    return token


@pytest.fixture
def authorized_client(client, auth_token):
    client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {auth_token}"
    return client
