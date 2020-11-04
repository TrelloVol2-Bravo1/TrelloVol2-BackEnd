from flask import Flask
from flask_cors import CORS
from flask_api import status
from flask import request

app = Flask(__name__)
CORS(app)


content = {'message': ''}

@app.route('/')
def getMessage():
    global content
    return content, status.HTTP_200_OK

@app.route('/', methods=['POST'])
def putMessage():
    req = request.get_json()
    global content
    content = {'message': req["message"]}
    return content, status.HTTP_200_OK

@app.route("/login", methods=['GET'])
def login():
    return 'Here we will have login page'

@app.route("/array_page/<array_id>", methods=['GET'])
def array(array_id):
    return 'Here we will have array page'

if __name__ == '__main__':
    app.run()
