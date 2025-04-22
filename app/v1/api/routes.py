from flask import Blueprint, Flask

from app.v1.views.auth_view import LoginAPI, RegisterAPI, VerifyEmailAPI
from app.v1.views.user_view import ProfileAPI

auth_blueprint_v1 = Blueprint("auth", __name__, url_prefix="/v1/auth")
auth_blueprint_v1.add_url_rule(
    "/register", view_func=RegisterAPI.as_view("register_api")
)
auth_blueprint_v1.add_url_rule("/login", view_func=LoginAPI.as_view("login_api"))
auth_blueprint_v1.add_url_rule(
    "/verify-email", view_func=VerifyEmailAPI.as_view("verify_email_api")
)

user_blueprint_v1 = Blueprint("user", __name__, url_prefix="/v1/users")
user_blueprint_v1.add_url_rule("/profile", view_func=ProfileAPI.as_view("profile_api"))


def register_v1_routes(app: Flask) -> None:
    app.register_blueprint(auth_blueprint_v1)
    app.register_blueprint(user_blueprint_v1)
