from Backend.resources.Card import CardsResource, CardResource, CardsListResource, CardMembersResource

def routes(register):
    register(CardsResource, '/card')
    register(CardResource, '/card/<int:card_id>')
    register(CardsListResource, '/cardList/<int:list_id>')
    register(CardMembersResource, '/cardMember')
