FROM python:3.8-alpine

RUN pip3 install gunicorn
RUN pip3 install flask
RUN pip3 install pycryptodome

WORKDIR /app

COPY app.py /app/
COPY run.sh /app/
COPY wsgi.py /app/
COPY templates /app/templates

COPY images /app/images

WORKDIR /app

ENTRYPOINT ["./run.sh"]