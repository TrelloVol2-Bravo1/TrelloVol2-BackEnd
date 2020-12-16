from Backend.resources.Card import CardsResource, CardResource, CardsListResource, CardMemberResource, CardMembersResource

def routes(register):
    register(CardsResource, '/card')
    register(CardResource, '/card/<int:card_id>')
    register(CardsListResource, '/cardList/<int:list_id>')
    register(CardMemberResource, '/cardMember')
    register(CardMembersResource, '/cardMembers/<int:card_id>')
