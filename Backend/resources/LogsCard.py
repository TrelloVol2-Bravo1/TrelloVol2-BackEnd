from flask_restful import reqparse, Resource, request

from Backend.resources.models.DBLogsCard import logs_schema

from Backend.resources.models.DBTable import DBTable
from Backend.resources.models.DBLogsCard import DBLogsCard

parser = reqparse.RequestParser()
parser.add_argument('log_id')
parser.add_argument('log_content')
parser.add_argument('user_id')
parser.add_argument('log_date')

class LogsCardResource(Resource):
    @staticmethod
    # @requireAuth
    def get(table_id):
        if table_id is None:
            return {'status_code': 'missing_data', 'message': 'There is no ID in request'}, 400

        table = DBTable.query.get(table_id)
        if table is None:
            return {'status_code': 'not_found', 'message': 'There is no Table with such ID'}, 404

        all_logs_card = DBLogsCard.query.filter(DBLogsCard.table_id == table_id).all()
        return {'status_code': 'success', 'data': logs_schema.dump(all_logs_card)}, 200
