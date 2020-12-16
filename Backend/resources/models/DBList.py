from Backend.db import db, ma
import re
from datetime import datetime
from uuid import uuid4
from passlib.apps import custom_app_context as pwd_context

from Backend.resources.models.DBAuth import DBAuth


class DBList(db.Model):
    __tablename__ = 'list'
    __table_args__ = {'extend_existing': True}

    list_id = db.Column(db.Integer, primary_key=True)
    list_name = db.Column(db.String(64), nullable=False)
    table_id = db.Column(db.Integer, index=True)
    list_order = db.Column(db.Integer)
    is_archived = db.Column(db.Integer, default=0)

    def setListName(self, newName):
        if newName is not None and len(newName) > 4 and self.list_name != newName:
            self.list_name = newName

    def setTableId(self, table_id):
        if table_id is not None:
            self.table_id = table_id

    def setIsArchived(self, is_archived):
        if is_archived is not None:
            self.is_archived = is_archived

    def setListOrder(self, list_order):
        if list_order is not None:
            self.list_order = list_order

    def updateList(self, args):
        results = list()
        results.append(self.setListName(args["list_name"]))
        results.append(self.setTableId(args["table_id"]))
        results.append(self.setIsArchived(args["is_archived"]))
        results.append(self.setListOrder(args["list_order"]))

        for result in results:
            if result != None:
                return result

    def putRequest(self, args):
        if args["list_name"] is None:
            return {'status_code': 'missing data',
                    "message": "There is no data to update"}, 400

        result = self.updateList(args)
        if result != None:
            return result

        db.session.add(self)
        db.session.commit()


    @staticmethod
    def register(args):
        list = DBList()

        # key = DBAuth.query.filter_by(user_id=request.headers.get('x-user-id'), api_key=request.headers.get('x-api-key')).first()
        #
        # if key is None:
        #     return {'status_code': 'failed', 'message': 'No such keys'}, 400

        result = list.updateList(args)
        if result != None:
            return result

        db.session.add(list)
        db.session.commit()

        return {'status_code': '201', 'message': 'List has been created', 'list': list_schema.dump(list)}, 201


class DBListSchema(ma.Schema):
    class Meta:
        fields = ('list_id', 'list_name', 'table_id', 'list_order', 'is_archived')


list_schema = DBListSchema()
lists_schema = DBListSchema(many=True)
