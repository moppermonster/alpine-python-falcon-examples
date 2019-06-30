'''
alpine-python-falcon example

This example adds a second "function" (class, resource instance and route).

This example also introduces resp.status
'''

import falcon
from middleware import JSONTranslator

class Hello_world(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.context["response"] = {"response": "Hello world"}

class Numbers(object):
    """Returns numbers"""
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.context["response"] = {"numbers": [1, 2, 3, 4]}

# Falcon
APP = falcon.API(middleware=[JSONTranslator()])

# Resource class instances
HELLO_WORLD = Hello_world()
NUMBERS = Numbers()

# Falcon routes
APP.add_route("/", HELLO_WORLD)
APP.add_route("/numbers", NUMBERS)
