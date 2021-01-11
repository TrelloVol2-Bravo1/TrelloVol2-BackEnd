from Backend.db import db, ma
import re
from datetime import datetime
from uuid import uuid4
from passlib.apps import custom_app_context as pwd_context

from Backend.resources.models.DBAuth import DBAuth


class DBTable(db.Model):
    __tablename__ = 'table'
    __table_args__ = {'extend_existing': True}

    table_id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String(64), nullable=False)
    table_description = db.Column(db.String(1024))
    user_id = db.Column(db.Integer, index=True)

    def setTableName(self, newName):
        if newName is not None and len(newName) > 4 and self.table_name != newName:
            self.table_name = newName

    def setUserId(self, user_id):
        if user_id is not None:
            self.user_id = user_id

    def setTableDescription(self, table_description):
        if table_description is not None:
            self.table_description = table_description

    def updateTable(self, args):
        results = list()
        results.append(self.setTableName(args["table_name"]))
        results.append(self.setTableDescription(args["table_description"]))
        results.append(self.setUserId(args["user_id"]))

        for result in results:
            if result != None:
                return result

    def putRequest(self, args):
        if args["table_name"] is None and args["table_description"] is None:
            return {'status_code': 'missing data',
                    "message": "There is no data to update"}, 400

        result = self.updateTable(args)
        if result != None:
            return result

        db.session.add(self)
        db.session.commit()

    @staticmethod
    def register(args):
        table = DBTable()

        # key = DBAuth.query.filter_by(user_id=request.headers.get('x-user-id'), api_key=request.headers.get('x-api-key')).first()
        #
        # if key is None:
        #     return {'status_code': 'failed', 'message': 'No such keys'}, 400

        result = table.updateTable(args)
        if result != None:
            return result

        db.session.add(table)
        db.session.commit()

        return {'status_code': '201', 'message': 'Table has been created', 'table': table_schema.dump(table)}, 201


class DBTableSchema(ma.Schema):
    class Meta:
        fields = ('table_id', 'table_name', 'table_description', 'user_id')


table_schema = DBTableSchema()
tables_schema = DBTableSchema(many=True)
