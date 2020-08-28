# Example 00 - Dockerfile and app.py

## Description
This is the most basic way to use the `alpine-python-falcon` image.

## How to
### Dockerfile
The first requirement is a `Dockerfile`.

This file has the following three lines:

```Dockerfile
FROM moppermonster/alpine-python-falcon

COPY app.py /app.py

CMD ["/usr/bin/supervisord"]
```

The line that starts with `FROM` tells Docker that the new *Docker image* we are writing should use the image `moppermonster/alpine-python-falcon` as it's base image.

Note the `moppermonster/` part: this means that the image is available on the *Docker Hub*. Docker will automatically download images from the Docker Hub if they aren't already present on your machine.

The line that starts with `COPY` tells Docker that we want to include the file `./app.py` in the image, at the location `/app.py`. This means that `app.py` will be available at `/app.py` within the container.

The line that starts with `CMD` tells Docker that whenever the container is started, the container should run the command `/usr/bin/supervisord`. This starts the `supervisord` program, which, simply put, manages our app for us.

> This is the last time the `FROM` and `CMD` are described, since they feature in every example.

### app.py
The second requirement is an `app.py` file.

This file has the following lines:
```python3
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
```

If you have worked with Falcon before, this is probably all you need to get started.

Let's go over the above example 'line by line':

#### falcon
```python3
import falcon
```
Obvious: import falcon so it can be used in the script.

#### middleware
```python3
from middleware import JSONTranslator
```
This imports the `JSONTranslator` Falcon *middleware*. This module is included by default in the `alpine-python-falcon` image and let's Falcon speak `json`.

Note that you can overwrite the default middleware by overwriting `/middleware.py` with your own `middleware.py` when you build your own image or start the container.

#### Hello_world()
```python3
class Hello_world(object):
    def on_get(self, req, resp):
        resp.context["response"] = {"response": "Hello world"}
```

Basic Falcon class. We define a name, and set `resp.context["response"]` to `{"response": "Hello world"}`.

Note how we define a method `on_get(self, req, resp)`, this means that our class can work with `GET` requests.

This is where we will run our code in upcoming examples. For now, all we do, is set `resp.context["response"]`, this sets the *response* Falcon will send when this class is called.

> Note that `"response"` in `{"response": "Hello world"}` could have been anything else `{"message": "Hello world"}`.

When we send a json request to the service using Python's `requests`:
```python3
>>> r = requests.get('http://localhost/', json={})
>>> r.json()['response']
'Hello world'
```

#### APP
```python3
APP = falcon.API(middleware=[JSONTranslator()])
```

This line is important as `APP` will be our main Falcon instance. What's also good to note is that we load our Falcon *middleware* here. Middleware was explained above.

`APP` is where we set Falcon *routes*.

#### Resource instances
```python3
HELLO_WORLD = Hello_world()
```

Resource instances. If the name alone doesn't tell you much: we "put" our `Hello_world()` class into `HELLO_WORLD`. That way, `HELLO_WORLD` becomes an *instance* of `Hello_world()`: allowing us to run whatever code we find in `Hello_world()` by setting a *path* to `HELLO_WORLD` as described below.

#### Routes
```python3
APP.add_route("/", HELLO_WORLD)
```

A *path* binds a *resource instance* to a, well, path. In the example line, the `HELLO_WORLD` instance is connected to `/`.

### Try it
If you don't fully follow yet, read up on the Falcon framework, that should make everything a lot clearer. Also be sure to check out the second example. It's description has way less text.

#### Start the container
For now, let's build the example image and start the container using `rebuild.sh`.

In the example directory, run `sh rebuild.sh`. Docker should build the image and start the container.

You can run the script again to remove the previously build version, build a new image and start a new container.

> Leave the container running! Tip: use a terminal "splitter" such as `tmux`.

The container runs on port 80 by default.

#### Talk to it
Let's talk json to the container.

- We'll import request. 
- Then we'll send a regular `GET` request to the service at `http://localhost`
- We'll print the response
- Next, we'll send a `json` `GET` request to the service at `http//localhost`
- We'll print the response again
- Finally, we'll print the string contained in the `json` dict we just received.

```python3
>>> import requests
>>> r = requests.get('http://localhost')
>>> r.json()
{'title': 'Empty request body. A valid JSON document is required.'}
>>> r = requests.get('http://localhost', json={})
>>> r.json()
{'response': 'Hello world'}
>>> r.json()['response']
'Hello world'
```
