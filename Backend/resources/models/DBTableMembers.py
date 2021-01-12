from Backend.db import db, ma


class DBTableMembers(db.Model):
    __tablename__ = 'table_members'
    __table_args__ = {'extend_existing': True}

    table_members_id = db.Column(db.Integer, primary_key=True)
    table_id = db.Column(db.Integer, index=True)
    user_id = db.Column(db.Integer, index=True)

    def setTableId(self, table_id):
        if table_id != None:
            self.table_id = table_id

    def setUserId(self, user_id):
        if user_id != None:
            self.user_id = user_id


    def register(self, table_id, user_id):
        if table_id is None:
            return {'status_code': 'failed', 'message': 'There is no table_id'}

        if user_id is None:
            return {'status_code': 'failed', 'message': 'There is no user_id'}

        self.setTableId(table_id)
        self.setUserId(user_id)
        db.session.add(self)
        db.session.commit()

        return {'table_id': self.table_id, 'user_id': self.user_id}


class DBTableMemberSchema(ma.Schema):
    class Meta:
        fields = ('table_id', 'user_id')

tableMemberSchema = DBTableMemberSchema
tablesMemberSchema = DBTableMemberSchema(many=True)