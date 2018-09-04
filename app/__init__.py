from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
import config

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'app.login'

pagedown = PageDown(app)

from app import views, models
