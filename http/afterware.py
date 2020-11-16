def afterware(response):
    response = setHeaders(response)
    return response

def setHeaders(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'content-type,x-api-key,x-user-id')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response