import desert
from flask import Response, current_app, jsonify, request
from flask.views import MethodView
from marshmallow import EXCLUDE
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest

from app.db.database import db
from app.v1.schemas.auth_schema import LoginRequest, RegisterRequest
from app.v1.services.auth_service import AuthService


class RegisterAPI(MethodView):
    def __init__(self) -> None:
        self.service = AuthService(
            session=db.session,
            rabbitmq_url=current_app.config["RABBITMQ_URL"],
            frontend_base_url=current_app.config["FRONTEND_BASE_URL"],
        )

    def post(self) -> tuple[Response, int]:
        try:
            post_data = request.get_json(silent=True) or {}
            schema = desert.schema(RegisterRequest, meta={"unknown": EXCLUDE})
            data = schema.load(post_data)
            self.service.register_user(data)
            return (
                jsonify(
                    {
                        "message": "Your email has been successfully registered. "
                        "Please check your email to verify email",
                    }
                ),
                201,
            )
        except ValidationError as e:
            return jsonify({"error": e.messages}), 400
        except Exception as e:
            print("error", str(e))
            return jsonify({"error": str(e)}), 500


class LoginAPI(MethodView):
    def __init__(self) -> None:
        self.service = AuthService(
            session=db.session,
            rabbitmq_url=current_app.config["RABBITMQ_URL"],
            frontend_base_url=current_app.config["FRONTEND_BASE_URL"],
        )

    def post(self) -> tuple[Response, int]:
        try:
            post_data = request.get_json(silent=True) or {}
            schema = desert.schema(LoginRequest, meta={"unknown": EXCLUDE})
            data = schema.load(post_data)

            res_data = self.service.authenticate_user(data)
            return (
                jsonify(
                    {
                        "message": "User registered successfully",
                        "access_token": res_data.access_token,
                        "token_type": res_data.token_type,
                    }
                ),
                200,
            )
        except ValidationError as e:
            return jsonify({"error": e.messages}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500


class VerifyEmailAPI(MethodView):
    def __init__(self) -> None:
        self.service = AuthService(
            session=db.session,
            rabbitmq_url=current_app.config["RABBITMQ_URL"],
            frontend_base_url=current_app.config["FRONTEND_BASE_URL"],
        )

    def get(self) -> tuple[Response, int]:
        """Verify user email from token"""
        try:
            token = request.args.get("token")
            if not token:
                raise BadRequest("Missing token")

            self.service.verify_email(token)
            return jsonify({"message": "Email verified successfully"}), 200

        except ValidationError as e:
            return jsonify({"error": e.messages}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
