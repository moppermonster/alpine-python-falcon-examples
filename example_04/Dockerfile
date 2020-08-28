FROM moppermonster/alpine-python-falcon

# Install requirements
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

COPY app.py /app.py
COPY myfunction.py /myfunction.py

CMD ["/usr/bin/supervisord"]
