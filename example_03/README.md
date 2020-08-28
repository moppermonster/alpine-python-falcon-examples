# Example 03 - Reading requests

## Description
In this example, we parse an incoming request for data.

## Dockerfile
`Dockerfile` remains the same.

```Dockerfile
FROM moppermonster/alpine-python-falcon

COPY app.py /app.py
COPY myfunction.py /myfunction.py

CMD ["/usr/bin/supervisord"]
```

## myfunction.py

```python3
def myfunction(numbers):
    """Adds up all ints in numbers and returns the result"""
    return sum(numbers)
```
A super simple function that takes a list, adds up the integers in that list and then returns the result.

## app.py

```python3
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
        request = (req.context['request'])
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
```

This `app.py` is, again, very similar to the previous example.

The `request = req.context['request']` line is new.

So far, we only worked with *response* (`resp`). We we can also work with *requests* (`req`).

The `req` object holds all *request* information. By reading from `req.context['request']` we are able to read json in requests like a regular dictionary.

## Usage

Let's rebuild and send a `POST` request containing some actual json.

```bash
sh rebuild.sh
```
> Leave the container running so we can connect to it!

```python3
>>> import requests
>>> r = requests.post('http://localhost/numbers', json={'numbers': [4, 4, 4, 3]})
>>> r.json()['result']
15
```
