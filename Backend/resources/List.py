from flask_restful import reqparse, Resource, request

from Backend.resources.models.DBList import DBList, list_schema, lists_schema
from Backend.db import db, ma

from Backend.resources.models.DBAuth import DBAuth
from Backend.resources.models.DBTable import DBTable

parser = reqparse.RequestParser()
parser.add_argument('list_id')
parser.add_argument('list_name')
parser.add_argument('table_id')

class ListResource(Resource):
    @staticmethod
    # @requireAuth
    def get(list_id):
        if list_id is None:
            return {'status_code': 'missing_data', 'message': 'There is no ID in request'}, 400

        # user = DBUser.query.filter_by(id=user_id).first()
        list = DBList.query.get(list_id)
        if list is None:
            return {'status_code': 'not_found', 'message': 'There is no List with such ID'}, 404

        if list == list.list_id:
            return {'status_code': 'success', 'data': list_schema.dump(list)}, 200

    @staticmethod
    def delete(list_id):
        list = DBList.query.get(list_id)

        if list_id is None:
            return {'status_code': 'missing_data', 'message': 'There is no ID in request'}, 400

        if list is None:
            return {'status_code': 'not_found', 'message': 'There is no List with such ID'}, 404

        if list_id == list.list_id:
            db.session.delete(list)
            db.session.commit()
            return {'status_code': 'success', 'message': 'List has been deleted'}, 200

    @staticmethod
    def put(list_id):
        args = parser.parse_args()
        list = DBList.query.get(list_id)

        if list_id is None:
            return {'status_code': 'missing_data', 'message': 'There is no ID in request'}, 400

        if list is None:
            return {'status_code': 'not_found', 'message': 'There is no List with such ID'}, 404

        result = list.putRequest(args)

        if result != None:
            return result

        return {'status_code': 'success', 'message': 'List has been updated'}, 200


class ListsResource(Resource):
    @staticmethod
    def get():
        all_lists = DBList.query.all()
        #key = DBAuth.query.filter_by(user_id=request.headers.get('x-user-id'), api_key=request.headers.get('x-api-key')).first()
        #if key is None:
        #    return {'status_code': 'failed', 'message': 'Permission denied'}, 400
        #all_tables = DBTable.query.filter_by(user_id=request.headers.get('x-user-id')).all()
        result = lists_schema.dump(all_lists)
        return {'status_code': 'success', 'data': result}, 200

    @staticmethod
    def post():
        args = parser.parse_args()
        #key = DBAuth.query.filter_by(user_id=request.headers.get('x-user-id'), api_key=request.headers.get('x-api-key')).first()
        #if key is None:
        #    return {'status_code': 'failed', 'message': 'Permission denied'}, 400
        #args["user_id"] = key.user_id

        result = DBList.register(args)
        if result != None:
            return result


class ListsTableResource(Resource):
    @staticmethod
    def get(table_id):
        lists_table = DBList.query.filter(DBList.table_id == table_id)
        result = lists_schema.dump(lists_table)
        return {'status_code': 'success', 'data': result}, 200
