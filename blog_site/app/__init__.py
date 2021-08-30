from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = "somegibberish"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/data.db'
csrf = CSRFProtect(app)
from . import routes