'''
alpine-python-falcon example

docker-compose example

Find out more: https://github.com/nielsds/alpine-python-falcon
'''

import falcon
from middleware import JSONTranslator

class Hello_compose(object):
    def on_get(self, req, resp):
        resp.context["response"] = {"response": "Hello docker-compose!"}

# Falcon
APP = falcon.API(middleware=[JSONTranslator()])

# Resource class instances
HELLO_COMPOSE = Hello_compose()

# Falcon routes
APP.add_route("/", HELLO_COMPOSE)
