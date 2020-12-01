from Backend.resources.Card import CardsResource, CardResource, CardsListResource

def routes(register):
    register(CardsResource, '/card')
    register(CardResource, '/card/<int:card_id>')
    register(CardsListResource, '/cardList/<int:list_id>')
