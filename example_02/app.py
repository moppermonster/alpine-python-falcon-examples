'''
alpine-python-falcon example

In this example, we import one of our own scripts: myfunction.

We then modify Numbers() to return myfunction.myfunction()'s result when we perform a POST request.

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
        result = myfunction([1, 2, 3, 4])
        resp.context["response"] = {"result": result}

# Falcon
APP = falcon.API(middleware=[JSONTranslator()])

# Resource class instances
HELLO_WORLD = Hello_world()
NUMBERS = Numbers()

# Falcon routes
APP.add_route("/", HELLO_WORLD)
APP.add_route("/numbers", NUMBERS)
