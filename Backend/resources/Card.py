from flask_restful import reqparse, Resource, request

from Backend.resources.models.DBCardMembers import DBCardMembers, cardsMemberSchema
from Backend.resources.models.DBCard import DBCard, card_schema, cards_schema
from Backend.resources.models.DBUser import DBUser
from Backend.resources.models.DBList import DBList
from Backend.resources.models.DBLogsCard import DBLogsCard
from Backend.db import db

from Backend.resources.models.DBAuth import DBAuth

parser = reqparse.RequestParser()
parser.add_argument('card_id')
parser.add_argument('card_name')
parser.add_argument('card_description')
parser.add_argument('list_id')
parser.add_argument('user_id')
parser.add_argument('card_deadline')
parser.add_argument('is_archived')
parser.add_argument('card_order')

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

        if card_id == card.card_id:
            return {'status_code': 'success', 'data': card_schema.dump(list)}, 200

    @staticmethod
    def delete(card_id):
        card = DBCard.query.get(card_id)

        if card_id is None:
            return {'status_code': 'missing_data', 'message': 'There is no ID in request'}, 400

        if card is None:
            return {'status_code': 'not_found', 'message': 'There is no Card with such ID'}, 404

        if card.is_archived == 0:
            return {'status_code': 'not archived', 'message': 'Card must be archived to be deleted'}, 400

        if card_id == card.card_id:
            cards_members = DBCardMembers.query.filter(DBCardMembers.card_id == card_id).all()
            for card_member in cards_members:
                db.session.delete(card_member)
                db.session.commit()

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

        key = DBAuth.query.filter_by(user_id=request.headers.get('x-user-id'),
                                     api_key=request.headers.get('x-api-key')).first()
        if key is None:
            return {'status_code': 'failed', 'message': 'Permission denied'}, 400
        args["user_id"] = key.user_id

        if args['card_name'] is None:
            args['card_name'] = DBCard.query.get(card_id).card_name

        if args['card_description'] is None:
            args['card_description'] = DBCard.query.get(card_id).card_description

        if args['list_id'] is None:
            args['list_id'] = DBCard.query.get(card_id).list_id

        if args['is_archived'] is None:
            args['is_archived'] = DBCard.query.get(card_id).is_archived

        if args['card_order'] is None:
            args['card_order'] = DBCard.query.get(card_id).card_order



        username = DBUser.query.get(args['user_id']).name
        table_id = DBList.query.get(args['list_id']).table_id

        log_object = DBLogsCard()
        log_object.user_id = args['user_id']
        log_object.table_id = table_id

        if int(card.list_id) != int(args['list_id']):
            previousListName = DBList.query.get(card.list_id).list_name
            nextListName = DBList.query.get(args['list_id']).list_name
            log_object.log_content = username + " moved " + args['card_name'] + " from " + previousListName + " to " + nextListName
            print(log_object.log_content)
            db.session.add(log_object)
            db.session.commit()

        if int(card.is_archived) == 0 and int(args['is_archived']) == 1:
            log_object.log_content = username + " archivized " + args['card_name']
            db.session.add(log_object)
            db.session.commit()

        elif int(card.is_archived) == 1 and int(args['is_archived']) == 0:
            log_object.log_content = username + " send " + args['card_name'] + " to board"
            db.session.add(log_object)
            db.session.commit()

        if card.card_name != args['card_name']:
            log_object.log_content = username + " changed name of " + card.card_name + " into " + args['card_name']
            db.session.add(log_object)
            db.session.commit()

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
        key = DBAuth.query.filter_by(user_id=request.headers.get('x-user-id'), api_key=request.headers.get('x-api-key')).first()
        if key is None:
           return {'status_code': 'failed', 'message': 'Permission denied'}, 400
        args["user_id"] = key.user_id

        username = DBUser.query.get(args['user_id']).name
        list_name = DBList.query.get(args['list_id']).list_name
        table_id = DBList.query.get(args['list_id']).table_id

        log_object = DBLogsCard()
        log_object.user_id = args['user_id']
        log_object.log_content = username + " added " + args['card_name'] + " to " + list_name
        log_object.table_id = table_id
        db.session.add(log_object)
        db.session.commit()

        result = DBCard.register(args)
        if result != None:
            return result


class CardsListResource(Resource):
    @staticmethod
    def get(list_id):
        cards_list = DBCard.query.filter(DBCard.list_id == list_id)
        result = cards_schema.dump(cards_list)
        return {'status_code': 'success', 'data': result}, 200


class CardMemberResource(Resource):
    @staticmethod
    def post():
        card_members = DBCardMembers()
        card_id = parser.parse_args()['card_id']
        user_id = parser.parse_args()['user_id']

        member = DBCardMembers.query.filter(DBCardMembers.card_id == card_id, DBCardMembers.user_id == user_id).first()
        if member is not None:
            return {'status code': 'failed', 'meassage': 'This user is actually connected with this card'}, 400

        result = card_members.register(card_id, user_id)

        return result, 200

    @staticmethod
    def delete():
        card_id = parser.parse_args()['card_id']
        user_id = parser.parse_args()['user_id']

        member = DBCardMembers.query.filter(DBCardMembers.card_id == card_id, DBCardMembers.user_id == user_id).first()
        if member is None:
            return {'status code': 'failed', 'meassage': 'This user is not connected with this card'}, 400

        db.session.delete(member)
        db.session.commit()

        return {'status code': 'success', "meassage": "Member deleted"}, 200

class CardMembersResource(Resource):
    @staticmethod
    def get(card_id):
        members = DBCardMembers.query.filter(DBCardMembers.card_id == card_id).all()
        result = cardsMemberSchema.dump(members)
        return {'status_code': 'success', 'data': result}, 200




