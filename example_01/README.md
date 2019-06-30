# Example 01 - Classes and resp

## Description
This example adds a second "function" (class, resource instance and route).

This example also introduces `resp.status`.

## Dockerfile
`Dockerfile` remains the same.

```Dockerfile
FROM dutchsecniels/alpine-python-falcon

COPY app.py /app.py

CMD ["/usr/bin/supervisord"]
```

## app.py

```python3
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
```

This `app.py` is very similar to the previous example.

The `rep.status` lines are completely new: they allow us to change the [http status code](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes). Here you can easily specify status codes such as (but not limited to!) *Bad Request* (400), *Forbidden* (403) or *Not Found* (404).

Using status codes makes it easy to quickly send a message about a request: in the usage example below, two ways of retreiving status codes with `requests` are demonstrated.

This file contains 2 *classes*; `Hello_world()` and `Numbers()`.

We used `Hello_world()` in the first example. Let's build the image, start the container and then use `python` to talk to the container.

## Usage

```bash
sh rebuild.sh
```
> Leave the container running so we can connect to it!

```python3
>>> import requests
>>> r = requests.get("http://localhost/", json={})
>>> r
<Response [200]>
>>> r.status_code
200
>>> r.json()
{'response': 'Hello world'}
>>> r = requests.get("http://localhost/numbers", json={})
>>> r
<Response [200]>
>>> r.json()
{'numbers': [1, 2, 3, 4]}
>>> r.json()['numbers']
[1, 2, 3, 4]
>>> r.json()['numbers'][1]
2
```
