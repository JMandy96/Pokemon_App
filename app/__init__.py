from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_migrate import Migrate
from .models import db, User

app = Flask(__name__)
app.config.from_object(Config)

login_manager = LoginManager()

db.init_app(app)
migrate = Migrate(app, db)
login_manager.init_app(app)

#login manager settings
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'danger'
login_manager.login_message = 'You must login to access that page.'

#import our blueprints
from app.blueprints.auth import auth
from app.blueprints.main import main

#register our blueprints
app.register_blueprint(main)
app.register_blueprint(auth)





@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

