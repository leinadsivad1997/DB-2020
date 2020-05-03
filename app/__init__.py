from flask import Flask
from flask_login import LoginManager
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = b'_5#y2L"oursecret\n\xec]/'

# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config.from_object(__name__)
from app import views
