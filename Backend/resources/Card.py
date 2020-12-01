from flask_restful import reqparse, Resource, request

from Backend.resources.models.DBCard import DBCard, card_schema, cards_schema
from Backend.db import db, ma

from Backend.resources.models.DBAuth import DBAuth
from Backend.resources.models.DBTable import DBTable

parser = reqparse.RequestParser()
parser.add_argument('card_id')
parser.add_argument('card_name')
parser.add_argument('card_description')
parser.add_argument('list_id')

class CardResource(Resource):
    @staticmethod
    # @requireAuth
    def get(card_id):
        if card_id is None:
            return {'status_code': 'missing_data', 'message': 'There is no ID in request'}, 400

        # user = DBUser.query.filter_by(id=user_id).first()
        card = DBCard.query.get(card_id)
        if card is None:
            return {'status_code': 'not_found', 'message': 'There is no Card with such ID'}, 404

        if card == card.card_id:
            return {'status_code': 'success', 'data': card_schema.dump(list)}, 200

    @staticmethod
    def delete(card_id):
        card = DBCard.query.get(card_id)

        if card_id is None:
            return {'status_code': 'missing_data', 'message': 'There is no ID in request'}, 400

        if card is None:
            return {'status_code': 'not_found', 'message': 'There is no Card with such ID'}, 404

        if card_id == card.card_id:
            db.session.delete(card)
            db.session.commit()
            return {'status_code': 'success', 'message': 'Card has been deleted'}, 200

    @staticmethod
    def put(card_id):
        args = parser.parse_args()
        card = DBCard.query.get(card_id)

        if card_id is None:
            return {'status_code': 'missing_data', 'message': 'There is no ID in request'}, 400

        if card is None:
            return {'status_code': 'not_found', 'message': 'There is no Card with such ID'}, 404

        result = card.putRequest(args)

        if result != None:
            return result

        return {'status_code': 'success', 'message': 'Card has been updated'}, 200


class CardsResource(Resource):
    @staticmethod
    def get():
        all_cards = DBCard.query.all()
        #key = DBAuth.query.filter_by(user_id=request.headers.get('x-user-id'), api_key=request.headers.get('x-api-key')).first()
        #if key is None:
        #    return {'status_code': 'failed', 'message': 'Permission denied'}, 400
        #all_tables = DBTable.query.filter_by(user_id=request.headers.get('x-user-id')).all()
        result = cards_schema.dump(all_cards)
        return {'status_code': 'success', 'data': result}, 200

    @staticmethod
    def post():
        args = parser.parse_args()
        #key = DBAuth.query.filter_by(user_id=request.headers.get('x-user-id'), api_key=request.headers.get('x-api-key')).first()
        #if key is None:
        #    return {'status_code': 'failed', 'message': 'Permission denied'}, 400
        #args["user_id"] = key.user_id

        result = DBCard.register(args)
        if result != None:
            return result

class CardsListResource(Resource):
    @staticmethod
    def get(list_id):
        cards_list = DBCard.query.filter(DBCard.list_id == list_id)
        result = cards_schema.dump(cards_list)
        return {'status_code': 'success', 'data': result}, 200