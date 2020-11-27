from flask import Flask
app = Flask('TrelloB')

from flask_cors import CORS
CORS(app)

from Backend.config import applyConfig
applyConfig(app)

from Backend.http.afterware import afterware
app.after_request(afterware)

from Backend.http.Router import Router
Router(app)

# Start a webserver
if __name__ == "__main__":
    app.run()
