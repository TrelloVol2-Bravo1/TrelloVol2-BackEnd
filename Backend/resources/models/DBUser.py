from Backend.db import db, ma
import re
from datetime import datetime
from passlib.apps import custom_app_context as pwd_context


class DBUser(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    access_level = db.Column(db.Integer, nullable=False, default=0)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def register(args):
        user = DBUser()

        result = user.updateUser(args)
        if result != None:
            return result

        db.session.add(user)
        db.session.commit()

        return {'status_code': '201', 'message': 'User has been created'}, 201

    def setUsername(self, newName):
        if newName is not None and len(newName) > 4 and self.name != newName:
            checkIfExists = DBUser.query.filter_by(name=newName).first()
            if checkIfExists is not None:
                return {'status_code': 'duplicate', 'message': 'User with such username already exists'}
            self.name = newName

    def setEmail(self, newMail):
        if newMail is not None and self.email != newMail:
            if not re.fullmatch(r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$", newMail):
                return {'status_code': 'invalid_mail', 'message': 'Wrong email address format'}, 400
            self.email = newMail

    def setPassword(self, newPassword):
        if newPassword is not None and len(newPassword) > 0:
            if len(newPassword) < 8:
                return {'status_code': 'weak_password',
                        'message': 'Password too weak'}, 400
            self.hash_password(newPassword)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, user_password):
        return pwd_context.verify(user_password, self.password_hash)

    def putRequest(self, args):
        if args["name"] is None and args["email"] is None and args["password"] is None:
            return {'status_code': 'missing data',
                    "message": "There is no data to update"}, 400

        result = self.updateUser(args)
        if result != None:
            return result

        db.session.add(self)
        db.session.commit()

    def updateUser(self, args):
        results = list()
        results.append(self.setUsername(args["name"].lower()))
        results.append(self.setEmail(args["email"].lower()))
        # results.append(self.setAccessLevel(args["access_level"]))
        results.append(self.setPassword(args["password"]))
        for result in results:
            if result != None:
                return result


class DBUserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'password', 'password_hash', 'access_level', 'creation_date')


user_schema = DBUserSchema()
users_schema = DBUserSchema(many=True)
