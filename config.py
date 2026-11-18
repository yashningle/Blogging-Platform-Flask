
import os


class Config:

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "dev-only-change-this-secret-key"
    )

    SQLALCHEMY_DATABASE_URI = "sqlite:///blog.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session Security
    SESSION_COOKIE_HTTPONLY = True

    SESSION_COOKIE_SAMESITE = "Lax"

    # Enable HTTPS security only in production
    SESSION_COOKIE_SECURE = (
        os.environ.get("FLASK_ENV") == "production"
    )
