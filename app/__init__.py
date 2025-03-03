"""Ink & Coffee Website initialization"""

import os
import secrets #generate a secure secret_key
from flask import Flask
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from dotenv import load_dotenv #The environmental variables will be loaded from this library


#Initialize the flask app
app = Flask(__name__)
load_dotenv()

#App configurations
app.config['DEBUG'] = True


#Accessing environment variables using os.getenv()
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET', secrets.token_hex(16))
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #suppresses a warning if true, avoid unnecessary overgead if false

#File upload configurations
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app', 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DEFAULT_BIO'] = 'There is no bio to show'


#Database initialization and user authentication
db = SQLAlchemy(app) #Initialize the database extension
migrate = Migrate(app, db)
bcryptHash = Bcrypt(app) #Initialize the Bcrypt extension for password hashing

#Flask login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = "info"  # customize the flash message category

#User loader function for Flask_login
@login_manager.user_loader
def load_user(user_id):
    from app.models import userAccount
    return userAccount.query.get(int(user_id))  



app.config.from_object(__name__)
from app import controller #models


