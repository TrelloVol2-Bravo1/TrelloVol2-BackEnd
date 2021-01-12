from flask_restful import reqparse, Resource, request

from Backend.db import db
from Backend.resources.models.DBAuth import DBAuth
from Backend.resources.models.DBTable import DBTable, table_schema, tables_schema
from Backend.resources.models.DBTableMembers import DBTableMembers

parser = reqparse.RequestParser()
parser.add_argument('table_id')
parser.add_argument('table_name')
parser.add_argument('table_description')
parser.add_argument('user_id')


class TableResource(Resource):
    @staticmethod
    # @requireAuth
    def get(table_id):
        if table_id is None:
            return {'status_code': 'missing_data', 'message': 'There is no ID in request'}, 400

        # user = DBUser.query.filter_by(id=user_id).first()
        table = DBTable.query.get(table_id)
        if table is None:
            return {'status_code': 'not_found', 'message': 'There is no Table with such ID'}, 404

        if table == table.table_id:
            return {'status_code': 'success', 'data': table_schema.dump(table)}, 200

    @staticmethod
    def delete(table_id):
        table = DBTable.query.get(table_id)

        if table_id is None:
            return {'status_code': 'missing_data', 'message': 'There is no ID in request'}, 400

        if table is None:
            return {'status_code': 'not_found', 'message': 'There is no Table with such ID'}, 404

        if table_id == table.table_id:
            db.session.delete(table)
            db.session.commit()
            table_members = DBTableMembers.query.filter(DBTableMembers.table_id == table_id).all()
            for table_member in table_members:
                db.session.delete(table_member)
                db.session.commit()
            return {'status_code': 'success', 'message': 'Card has been deleted'}, 200

    @staticmethod
    def put(table_id):
        args = parser.parse_args()
        table = DBTable.query.get(table_id)

        if table_id is None:
            return {'status_code': 'missing_data', 'message': 'There is no ID in request'}, 400

        if table is None:
            return {'status_code': 'not_found', 'message': 'There is no Table with such ID'}, 404

        result = table.putRequest(args)

        if result != None:
            return result

        return {'status_code': 'success', 'message': 'Table has been updated'}, 200


class TablesResource(Resource):
    @staticmethod
    def get():
        # all_tables = DBTable.query.all()
        key = DBAuth.query.filter_by(user_id=request.headers.get('x-user-id'),
                                     api_key=request.headers.get('x-api-key')).first()
        if key is None:
            return {'status_code': 'failed', 'message': 'Permission denied'}, 400
        all_table_members = DBTableMembers.query.filter_by(user_id=request.headers.get('x-user-id')).all()
        print(request.headers.get('x-user-id'))
        print(all_table_members)
        all_tables = []
        for x in all_table_members:
            all_tables.append(DBTable.query.get(x.table_id))
        result = tables_schema.dump(all_tables)
        return {'status_code': 'success', 'data': result}, 200

    @staticmethod
    def post():
        args = parser.parse_args()
        key = DBAuth.query.filter_by(user_id=request.headers.get('x-user-id'),
                                     api_key=request.headers.get('x-api-key')).first()
        if key is None:
            return {'status_code': 'failed', 'message': 'Permission denied'}, 400
        args["user_id"] = key.user_id

        result = DBTable.register(args)

        newTableMember = DBTableMembers()
        newTableMember.setTableId(result[0]['table']['table_id'])
        newTableMember.setUserId(args["user_id"])
        db.session.add(newTableMember)
        db.session.commit()
        if result != None:
            return result

class TableMembersResource(Resource):
    @staticmethod
    def post():
        table_members = DBTableMembers()
        table_id = parser.parse_args()['table_id']
        user_id = parser.parse_args()['user_id']

        member = DBTableMembers.query.filter(DBTableMembers.table_id == table_id, DBTableMembers.user_id == user_id).first()
        if member is not None:
            return {'status code': 'failed', 'meassage': 'This user is actually connected with this table'}, 400

        result = table_members.register(table_id, user_id)

        return result, 200

    @staticmethod
    def delete():
        table_id = parser.parse_args()['table_id']
        user_id = parser.parse_args()['user_id']

        member = DBTableMembers.query.filter(DBTableMembers.table_id == table_id, DBTableMembers.user_id == user_id).first()
        if member is None:
            return {'status code': 'failed', 'meassage': 'This user is not connected with this table'}, 400

        db.session.delete(member)
        db.session.commit()

        return {'status code': 'success', "meassage": "Member deleted"}, 200