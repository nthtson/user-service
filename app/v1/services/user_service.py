from typing import Optional

from sqlalchemy.orm.scoping import scoped_session

from app.core.error_handlers import ErrorCreatingUserException, UserNotFoundException
from app.v1.models import User
from app.v1.repositories.user_repository import UserRepository
from app.v1.schemas.user_schema import UserUpdateRequest


class UserService:
    def __init__(self, session: scoped_session):
        self.user_repo = UserRepository(session)

    def get_user_profile(self, user_id: int) -> User:
        try:
            user: Optional[User] = self.user_repo.get_user_by_id(user_id)
            if not user:
                raise UserNotFoundException()

            return user
        except Exception as e:
            raise ErrorCreatingUserException(f"Error registering user: {str(e)}")

    def update_user(self, user_id: int, data: UserUpdateRequest) -> Optional[User]:
        update_data = data.__dict__
        update_data = {k: v for k, v in update_data.items() if v is not None}
        return self.user_repo.update_user(user_id, **update_data)
