from Backend.db import db


class DBCardMembers(db.Model):
    __tablename__ = 'card_members'
    __table_args__ = {'extend_existing': True}

    card_members_id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, index=True)
    user_id = db.Column(db.Integer, index=True)

    def setCardId(self, card_id):
        if card_id != None:
            self.card_id = card_id

    def setUserId(self, user_id):
        if user_id != None:
            self.user_id = user_id


    def register(self, card_id, user_id):
        if card_id is None:
            return {'status_code': 'failed', 'message': 'There is no card_id'}

        if user_id is None:
            return {'status_code': 'failed', 'message': 'There is no user_id'}

        self.setCardId(card_id)
        self.setUserId(user_id)
        db.session.add(self)
        db.session.commit()

        return {'card_id': self.card_id, 'user_id': self.user_id}
