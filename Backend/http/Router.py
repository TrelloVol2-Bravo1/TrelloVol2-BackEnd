from Backend.http.FlaskAPI import FlaskAPI
from importlib import import_module

class Router:
    """This class exists as a helper to organise all the API routing"""

    def __init__(self, app):
        self.api = FlaskAPI(app)
        loadRoutes = getListOfRoutes()
        list(map(self.loadRouteCategory, loadRoutes))

    def loadRouteCategory(self, routeModule):
        return dynImportRouteFunc(routeModule)(self.register)

    def register(self, resource, route):
        self.api.add_resource(resource, route)

def dynImportRouteFunc(route):
    try:
        return import_module("Backend.http.routes." + route).routes
    except Exception as e:
        ## Printing wont work in Flask
        ## Could clog up the thread since it waits for flask app to stop
        #print("Error dynamically importing module: " + route +"\n" + str(e))
        raise

def getListOfRoutes():
    from os.path import dirname, basename, isfile, join
    import glob
    modules = glob.glob(join(dirname(__file__) + "/routes/", "*.py"))
    return [
        basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')
    ]