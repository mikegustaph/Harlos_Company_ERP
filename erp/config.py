from datetime import timedelta

DEBUG = True
SECRET_KEY = "da259f16dc0f4b8c81e02cf2459ece65"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
MAIL_SERVER = "mail.harloscontainers.com"
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = "noreply@harloscontainers.com"
MAIL_PASSWORD = "harlos2016"
WEB_URL = "https://harloscontainers.com/"
# PERMANENT_SESSION_LIFETIME = timedelta(minutes=5)
