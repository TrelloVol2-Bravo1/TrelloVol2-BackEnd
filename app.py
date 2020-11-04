from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route("/login", methods=['GET'])
def login():
    return 'Here we will have login page'

@app.route("/array_page/<array_id>", methods=['GET'])
def array(array_id):
    return 'Here we will have array page'

if __name__ == '__main__':
    app.run()
