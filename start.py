from flask import Flask
app = Flask('TrelloB')

from flask_cors import CORS
CORS(app)

from TrelloB.config import applyConfig
applyConfig(app)

from TrelloB.http.afterware import afterware
app.after_request(afterware)

from TrelloB.http.Router import Router
Router(app)

# Start a webserver
if __name__ == "__main__":
    from werkzeug.serving import run_simple
    run_simple("localhost", 5000, app, use_debugger=False)
