from flask_restful import reqparse, Resource, request

from Backend.resources.models.DBTable import DBTable, table_schema, tables_schema
from Backend.db import db, ma

from Backend.resources.models.DBAuth import DBAuth

parser = reqparse.RequestParser()
parser.add_argument('table_id')
parser.add_argument('table_name')
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
            return {'status_code': 'success', 'message': 'Table has been deleted'}, 200

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
        key = DBAuth.query.filter_by(user_id=request.headers.get('x-user-id'), api_key=request.headers.get('x-api-key')).first()
        if key is None:
            return {'status_code': 'failed', 'message': 'Permission denied'}, 400
        all_tables = DBTable.query.filter_by(user_id=request.headers.get('x-user-id')).all()
        result = tables_schema.dump(all_tables)
        return {'status_code': 'success', 'data': result}, 200

    @staticmethod
    def post():
        args = parser.parse_args()
        key = DBAuth.query.filter_by(user_id=request.headers.get('x-user-id'), api_key=request.headers.get('x-api-key')).first()
        if key is None:
            return {'status_code': 'failed', 'message': 'Permission denied'}, 400
        args["user_id"] = key.user_id

        result = DBTable.register(args)
        if result != None:
            return result
