from Backend.db import db, ma


class DBCard(db.Model):
    __tablename__ = 'card'
    __table_args__ = {'extend_existing': True}

    card_id = db.Column(db.Integer, primary_key=True)
    card_name = db.Column(db.String(64), nullable=False)
    card_description = db.Column(db.String(1028), nullable=True)
    list_id = db.Column(db.Integer, index=True)

    def setCardName(self, newName):
        if newName is not None and len(newName) > 4 and self.card_name != newName:
            self.card_name = newName

    def setListId(self, list_id):
        if list_id is not None:
            self.list_id = list_id

    def setCardDescription(self, newDescription):
        if newDescription is not None and len(newDescription) > 4 and self.card_description != newDescription:
            self.card_description = newDescription


    def updateCard(self, args):
        results = list()
        results.append(self.setCardName(args["card_name"]))
        results.append(self.setCardDescription(args["card_description"]))
        results.append(self.setListId(args["list_id"]))

        for result in results:
            if result != None:
                return result

    def putRequest(self, args):
        if args["card_name"] is None:
            return {'status_code': 'missing data',
                    "message": "There is no data to update"}, 400

        result = self.updateCard(args)
        if result != None:
            return result

        db.session.add(self)
        db.session.commit()

    @staticmethod
    def register(args):
        card = DBCard()

        # key = DBAuth.query.filter_by(user_id=request.headers.get('x-user-id'), api_key=request.headers.get('x-api-key')).first()
        #
        # if key is None:
        #     return {'status_code': 'failed', 'message': 'No such keys'}, 400

        result = card.updateCard(args)
        if result != None:
            return result

        db.session.add(card)
        db.session.commit()

        return {'status_code': '201', 'message': 'Card has been created', 'list': card_schema.dump(card)}, 201


class DBCardSchema(ma.Schema):
    class Meta:
        fields = ('card_id', 'card_name', 'card_description', 'list_id')


card_schema = DBCardSchema()
cards_schema = DBCardSchema(many=True)
