from Backend.db import db, ma
from datetime import datetime

class DBLogsCard(db.Model):
    __tablename__ = 'logs_card'
    __table_args__ = {'extend_existing': True}

    log_id = db.Column(db.Integer, primary_key=True)
    log_content = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, index=True)
    table_id = db.Column(db.Integer, index=True)
    log_date = db.Column(db.DATETIME, default=datetime.utcnow())

    @staticmethod
    def register(args):

        return {'status_code': '201', 'message': 'Card has been created', 'list': logs_schema.dump()}, 201

class DBLogsCardSchema(ma.Schema):
    class Meta:
        fields = ('log_id', 'log_content', 'user_id', 'log_date', 'table_id')


log_schema = DBLogsCardSchema
logs_schema = DBLogsCardSchema(many=True)
