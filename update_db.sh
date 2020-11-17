rm db.sqlite
sqlite3 db.sqlite < db.sqlite.sql
FLASK_APP=start.py FLASK_DEBUG=1 python3 -m flask run