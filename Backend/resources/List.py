from flask_restful import reqparse, Resource, request

from Backend.resources.models.DBList import DBList, list_schema, lists_schema
from Backend.db import db

parser = reqparse.RequestParser()
parser.add_argument('list_id')
parser.add_argument('list_name')
parser.add_argument('table_id')
parser.add_argument('list_order')
parser.add_argument('list_description')
parser.add_argument('is_archived')


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

        if list.is_archived == 0:
            return {'status_code': 'not archived', 'message': 'List must be archived to be deleted'}, 400

        if list_id == list.list_id:
            db.session.delete(list)
            db.session.commit()
            return {'status_code': 'success', 'message': 'List has been deleted'}, 200

    @staticmethod
    def put(list_id):
        args = parser.parse_args()
        list_object = DBList.query.get(list_id)

        if list_id is None:
            return {'status_code': 'missing_data', 'message': 'There is no ID in request'}, 400

        if list_object is None:
            return {'status_code': 'not_found', 'message': 'There is no Table with such ID'}, 404

        result = list_object.putRequest(args)

        if result is not None:
            return result

        return {'status_code': 'success', 'message': 'List has been updated'}, 200


        # actual_list_order = list.list_order
        # given_list_order = int(args['list_order'])
        # table_id = args['table_id']
        # lists = DBList.query.filter(DBList.table_id == table_id).group_by(DBList.list_order).all()
        #
        # print(given_list_order)
        # print(actual_list_order)
        #
        # if given_list_order < actual_list_order:
        #     for i in range(given_list_order - 1, len(lists)):
        #         lists[i].setListOrder(i + 2)
        #         db.session.add(lists[i])
        #         db.session.commit()
        #         print(i)
        #
        # if given_list_order > actual_list_order:
        #     for i in range(given_list_order - 1, actual_list_order - 2, -1):
        #         lists[i].setListOrder(i)
        #         db.session.add(lists[i])
        #         db.session.commit()
        #         print(i)



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


        #autoinkrementacja kolejności list w tablicy
        table_id = args['table_id']
        lists = DBList.query.filter(DBList.table_id == table_id).all()
        args['list_order'] = len(lists) + 1

        result = DBList.register(args)
        if result != None:
            return result


class ListsTableResource(Resource):
    @staticmethod
    def get(table_id):
        lists_table = DBList.query.filter(DBList.table_id == table_id).group_by(DBList.list_order).all()
        result = lists_schema.dump(lists_table)
        return {'status_code': 'success', 'data': result}, 200
