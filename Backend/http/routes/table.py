from Backend.resources.Table import TableResource, TablesResource


def routes(register):
    register(TablesResource, '/table')
    register(TableResource, '/table/<int:table_id>')
