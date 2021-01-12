from Backend.resources.Card import CardsResource, CardResource, CardsListResource, CardMemberResource, CardMembersResource
from Backend.resources.LogsCard import LogsCardResource

def routes(register):
    register(CardsResource, '/card')
    register(CardResource, '/card/<int:card_id>')
    register(CardsListResource, '/cardList/<int:list_id>')
    register(CardMemberResource, '/cardMember')
    register(CardMembersResource, '/cardMembers/<int:card_id>')
    register(LogsCardResource, '/logsCard/<int:table_id>')
