import os
from flask import g
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / 'config.env'
load_dotenv(dotenv_path=env_path)

def applyConfig(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    app.config['SECURITY_PASSWORD_SALT'] = 'secret-password'
    app.config['SECRET_KEY'] = 'secret-key'

    app.config['ROOT_DIR'] = os.path.dirname(os.path.abspath(__file__))