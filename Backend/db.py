from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from Backend.app import app

db = SQLAlchemy(app)
db.app = app
db.init_app(app)
db.create_all()

ma = Marshmallow()
