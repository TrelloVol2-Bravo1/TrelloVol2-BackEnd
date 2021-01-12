from Backend.resources.Table import TableResource, TablesResource, TableMembersResource


def routes(register):
    register(TablesResource, '/table')
    register(TableResource, '/table/<int:table_id>')
    register(TableMembersResource, '/tablemember')