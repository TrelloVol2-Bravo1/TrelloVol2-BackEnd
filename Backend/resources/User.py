from flask_restful import reqparse, Resource, request

from Backend.resources.models.DBUser import DBUser, user_schema, users_schema
from Backend.db import db

from Backend.resources.models.DBAuth import DBAuth

parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('name')
parser.add_argument('password')
parser.add_argument('email')
parser.add_argument('access_level')
parser.add_argument('creation_date')
parser.add_argument('api_key')
parser.add_argument('api_date')


class UserResource(Resource):
    @staticmethod
    # @requireAuth
    def get(user_id):
        if user_id is None:
            return {'status_code': 'missing_data', 'message': 'There is no ID in request'}, 400

        # user = DBUser.query.filter_by(id=user_id).first()
        user = DBUser.query.get(user_id)
        if user is None:
            return {'status_code': 'not_found', 'message': 'There is no user with such ID'}, 404

        if user_id == user.id:
            return {'status_code': 'success', 'data': user_schema.dump(user)}, 200

    @staticmethod
    def delete(user_id):
        user = DBUser.query.get(user_id)

        if user_id is None:
            return {'status_code': 'missing_data', 'message': 'There is no ID in request'}, 400

        if user is None:
            return {'status_code': 'not_found', 'message': 'There is no user with such ID'}, 404

        if user_id == user.id:
            db.session.delete(user)
            db.session.commit()
            return {'status_code': 'success', 'message': 'User has been deleted'}, 200

    @staticmethod
    def put(user_id):
        args = parser.parse_args()
        user = DBUser.query.get(user_id)

        if user_id is None:
            return {'status_code': 'missing_data', 'message': 'There is no ID in request'}, 400

        if user is None:
            return {'status_code': 'not_found', 'message': 'There is no user with such ID'}, 404

        result = user.putRequest(args)

        if result != None:
            return result

        return {'status_code': 'success', 'message': 'User has been updated'}, 200


class UsersResource(Resource):
    @staticmethod
    def get():
        all_users = DBUser.query.all()
        result = users_schema.dump(all_users)
        return {'status_code': 'success', 'data': result}, 200

    @staticmethod
    def post():
        args = parser.parse_args()

        result = DBUser.register(args)
        if result != None:
            return result


class UserAuth(Resource):
    @staticmethod
    def post():  # login
        args = parser.parse_args()
        if args["name"] == None or args["password"] == None:
            return {'status_code': 'missing_data', 'message': 'There is no username or password in request'}, 400

        auth = DBAuth()
        user = DBUser.query.filter_by(name=args['name'].lower()).first()
        result = auth.loginAttempt(user, args['password'])

        if 'status_code' in result and result['status_code'] == 'auth_fail':
            return result, 400

        return {'status_code': 'success', 'message': ' You have been logged in', 'api_key': result["api_key"],
                'user_id': result["user_id"]}, 201
    @staticmethod
    def delete(): # logout
        key = DBAuth.query.filter_by(user_id=request.headers.get('x-user-id'), api_key=request.headers.get('x-api-key')).first()

        if key is None:
             return {'status_code': 'failed', 'message': 'No such keys'}, 400

        db.session.delete(key)
        db.session.commit()
        return {'status_code': 'success', 'message': 'Your api key has been deleted'}, 200

class Username(Resource):
    @staticmethod
    def get(user_id):
        if user_id is None:
            return {'status_code': 'missing_data', 'message': 'There is no ID in request'}, 400

        user = DBUser.query.get(user_id)
        if user is None:
            return {'status_code': 'not_found', 'message': 'There is no user with such ID'}, 404

        if user_id == user.id:
            return {'username': user.name}, 200

