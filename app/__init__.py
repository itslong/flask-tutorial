from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


"""
One aspect that may seem confusing at first is that there are two entities named app. 
The app package is defined by the app directory and the __init__.py script, 
and is referenced in the from app import routes statement. 
The app variable is defined as an instance of class Flask in the __init__.py script, 
which makes it a member of the app package.
"""
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

# import down here to prevent circular imports
# app import is from flask, not the variable
from app import routes, models
