import logging

from flask import Blueprint, Response, jsonify
from werkzeug.exceptions import HTTPException

error_handler_bp = Blueprint("error_handlers", __name__)
logger = logging.getLogger(__name__)


@error_handler_bp.app_errorhandler(HTTPException)
def handle_http_exception(e: HTTPException) -> tuple[Response, int]:
    logger.warning("HTTP Exception: %s - %s", e.name, e.description)
    response = {
        "error": {
            "type": e.name,
            "message": e.description,
            "code": e.code,
        }
    }
    return jsonify(response), e.code or 500


@error_handler_bp.app_errorhandler(Exception)
def handle_generic_exception(e: Exception) -> tuple[Response, int]:
    logger.exception("Unhandled exception: %s", str(e))
    response = {
        "error": {
            "type": "InternalServerError",
            "message": "An unexpected error occurred.",
        }
    }
    return jsonify(response), 500


class UserNotFoundException(Exception):
    pass


class ValidationException(Exception):
    pass


class NotFoundException(Exception):
    pass


class ErrorVerifyingEmailException(Exception):
    pass


class ErrorCreatingUserException(Exception):
    pass
