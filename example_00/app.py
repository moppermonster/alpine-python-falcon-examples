'''
alpine-python-falcon example

You can use this file as a starting point for building your own services

This example assumes use of the built in JSONTranslator Falcon middleware

Find out more: https://github.com/nielsds/alpine-python-falcon
'''

import falcon
from middleware import JSONTranslator

class Hello_world(object):
    def on_get(self, req, resp):
        resp.context["response"] = {"response": "Hello world"}

# Falcon
APP = falcon.API(middleware=[JSONTranslator()])

# Resource class instances
HELLO_WORLD = Hello_world()

# Falcon routes
APP.add_route("/", HELLO_WORLD)
