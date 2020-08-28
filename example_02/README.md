# Example 02 - imports and on_post()

## Description
In this example, we import one of our own scripts: `myfunction`.

This example adds a second method to `Numbers()` from the previous example.

## Dockerfile
`Dockerfile` remains the almost the same, we'll have to specify that we want to `COPY` `myfunction.py` to be abe to use it within the container.

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
```

This `app.py` is very similar to the previous example.

Since we included `myfunction.py` in our image, we can now simply import it.

To add support for `POST` requests, all we need to do is create a `on_post()` method. Since we are working within the `Numbers()` class we specified before, we don't have to perform actions such as setting paths again.

## Usage

Let's rebuild and send a `POST` request.

```bash
sh rebuild.sh
```
> Leave the container running so we can connect to it!

```python3
>>> import requests
>>> r = requests.get("http://localhost/numbers", json={})
>>> r.json()
{'numbers': [1, 2, 3, 4]}
>>> r = requests.post("http://localhost/numbers", json={})
>>> r.json()
{'result': 10}
>>> r.json()['result']+32
42
```
