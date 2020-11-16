from TrelloB.db import db, ma
import re
from datetime import datetime
from uuid import uuid4
from passlib.apps import custom_app_context as pwd_context


class DBAuth(db.Model):
    __tablename__ = 'auth'
    __table_args__ = {'extend_existing': True}

    api_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True)
    api_key = db.Column(db.String(256))
    api_date = db.Column(db.DateTime, default=datetime.utcnow)

    def generate_key(self, user_id):
        self.user_id = user_id
        self.api_key = uuid4().hex
        self.api_date = datetime.utcnow()
        return self.api_key

    def loginAttempt(self, user, password):
        if user is None:
            return {'status_code': 'auth_fail', 'message': 'There is no such user'}

        if not user.verify_password(password):
            return {'status_code': 'auth_fail', 'message': 'Wrong password'}

        self.generate_key(user.id)
        db.session.add(self)
        db.session.commit()
        return { 'api_key': self.api_key, 'user_id': user.id }