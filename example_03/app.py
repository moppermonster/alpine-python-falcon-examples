'''
alpine-python-falcon example

Here, we modify Numbers()'s on_get() method to read json instead of reading numbers from a list.

'''

import falcon
from middleware import JSONTranslator
from myfunction import myfunction

class Hello_world(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.context["response"] = {"response": "Hello world"}

class Numbers(object):
    """Returns numbers"""
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.context["response"] = {"numbers": [1, 2, 3, 4]}

    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200
        request = req.context['request']
        result = myfunction(request['numbers'])
        resp.context["response"] = {"result": result}

# Falcon
APP = falcon.API(middleware=[JSONTranslator()])

# Resource class instances
HELLO_WORLD = Hello_world()
NUMBERS = Numbers()

# Falcon routes
APP.add_route("/", HELLO_WORLD)
APP.add_route("/numbers", NUMBERS)
