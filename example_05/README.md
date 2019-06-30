# Example 05 - docker-compose

## Description
This example uses `docker-compose` to overwrite files in the existing container. Therefore, this example does not require building it's own container.

## How to
### docker-compose
The first requirement is a `Dockerfile`.

This file has the following three lines:

```yaml
version: '3.2'
services:
  example05:
    image: 'dutchsecniels/alpine-python-falcon'
    ports:
       - "80:80"
    volumes:
       - ${PWD}/app.py:/app.py
```

This `docker-compose.yml` file uses the original image from the Docker hub.

Using Docker-compose we mount the file `.app.py` over the existing `/app.py` file within the container.

We also specify the `port` this service should run on.

> Note: This is a very simple `docker-compose` example.

## app.py

We simply modified the original example `app.py` to say `Hello docker-compose!` instead of `Hello world!`.

```python3
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
```

## Usage

When we are in the same directory as the `docker-compose.yml` file we can simply start our service with:
```bash
docker-compose up
```

Using `requests` again:

```python3
>>> import requests
>>> r = requests.get('http://localhost', json={})
>>> r.json()
{'response': 'Hello docker-compose!'}
```

