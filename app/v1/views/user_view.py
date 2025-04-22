import logging

import desert
from flask import Response, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import EXCLUDE

from app.core.error_handlers import UserNotFoundException
from app.db.database import db
from app.v1.schemas.user_schema import UserUpdateRequest
from app.v1.services.user_service import UserService

logger = logging.getLogger(__name__)


class ProfileAPI(MethodView):
    def __init__(self) -> None:
        self.user_service = UserService(session=db.session)

    @jwt_required()
    def get(self) -> tuple[Response, int] | Response:
        """
        Get the current user's profile based on JWT authentication
        """
        try:
            user_id = get_jwt_identity()
            user = self.user_service.get_user_profile(user_id=user_id)
            return jsonify(user.to_dict())
        except UserNotFoundException:
            return jsonify({"error": "User not found"}), 404

    @jwt_required()
    def put(self) -> tuple[Response, int] | Response:
        try:
            user_id = get_jwt_identity()
            post_data = request.get_json(silent=True) or {}
            schema = desert.schema(UserUpdateRequest, meta={"unknown": EXCLUDE})
            update_data = schema.load(post_data)
            user = self.user_service.update_user(user_id, update_data)
            if not user:
                return jsonify({"message": "User not found"}), 404
            return jsonify(
                {"message": "User updated successfully", "user": user.to_dict()}
            )
        except Exception as e:
            logger.error(f"Error updating user: {e}")
            return jsonify({"message": "Error updating user"}), 500
