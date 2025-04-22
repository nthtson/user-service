import sentry_sdk
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration


def init_sentry(app: Flask) -> None:
    sentry_dsn = app.config.get("SENTRY_DSN")
    if sentry_dsn:
        sentry_sdk.init(
            dsn=sentry_dsn,
            integrations=[FlaskIntegration()],
            traces_sample_rate=1.0,
            environment=app.config.get("ENV", "development"),
        )
