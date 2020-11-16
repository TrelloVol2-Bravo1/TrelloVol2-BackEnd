from flask import jsonify
from flask_restful import Api
from werkzeug.exceptions import HTTPException
from TrelloB.start import app

class FlaskAPI(Api):
    def error_router(self, original_handler, e):
        return self.handle_error(e)

    def handle_error(self, e):
        if isinstance(e, HTTPException):
            if e.code == 400:
                return jsonify({'status_code': 'bad_request', 'message': 'This action is not valid'}), 400
            if e.code == 404:
                return jsonify({'status_code': 'not_found', 'message': 'This action is not defined'}), 404
            elif e.code == 405:
                return jsonify({'status_code': 'not_allowed', 'message': 'This action is not allowed'}), 405
            else:
                return jsonify({'message': str(e)}), e.code

        if app.config['DEBUG'] == True:
            raise e # when we are in debugmode simply raise all non HTTPExceptions
