# Example 04 - requirements.txt

## Description
In this example, we introduce a function that requires us to install some extra packages from a `requirements.txt` file.

## requirements.txt
This file is required for the next step.
```
requests
```

## Dockerfile
This time, the `Dockerfile` requires a few extra lines.

```Dockerfile
FROM moppermonster/alpine-python-falcon

# Install requirements
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

COPY app.py /app.py
COPY myfunction.py /myfunction.py

CMD ["/usr/bin/supervisord"]
```

This `Dockerfile` now also copies `./requirements.txt`. This installs any modules listed in the file into the image.

## myfunction.py

```python3
import requests

def myfunction(numbers):
    """Adds up all ints in numbers and returns the result"""
    return sum(numbers)

def awesomefunction():
    """Returns stuff!"""
    r = requests.get('http://localhost/', json={})
    return r.json()
```
`awesomefunction()` requires the `requests` module. Luckily, we installed the module from our `Dockerfile`.

## app.py

```python3
import falcon
from middleware import JSONTranslator
from myfunction import myfunction, awesomefunction

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

    def on_put(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.context["response"] = {"awesome": awesomefunction()}
# Falcon
APP = falcon.API(middleware=[JSONTranslator()])

# Resource class instances
HELLO_WORLD = Hello_world()
NUMBERS = Numbers()

# Falcon routes
APP.add_route("/", HELLO_WORLD)
APP.add_route("/numbers", NUMBERS)

```

This time, we defined `on_post()`. This will call the `awesomefunction`, which is now being imported in the third line in the above example.

## Usage

Let's rebuild and send a `PUT` request to `http://localhost/numbers`.

```bash
sh rebuild.sh
```
> Leave the container running so we can connect to it!

```python3
>>> import requests
>>> r = requests.put("http://localhost/numbers", json={})
>>> r
<Response [200]>
>>> r.json()
{'awesome': {'response': 'Hello world'}}
```

> Notice that we our `awesomefunction` just ran a `GET` requests against `http://localhost/` from within the container. Take a look at the containers log to see what just happened!

```
worker 1 killed successfully (pid: 12)
uWSGI worker 1 cheaped.
```
