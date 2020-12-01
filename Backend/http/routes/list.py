from Backend.resources.List import ListsResource, ListResource, ListsTableResource

def routes(register):
    register(ListsResource, '/list')
    register(ListResource, '/list/<int:list_id>')
    register(ListsTableResource, '/listTable/<int:table_id>')
