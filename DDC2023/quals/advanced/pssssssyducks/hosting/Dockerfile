FROM python:3.6.12-alpine

RUN pip3 install gunicorn
RUN pip3 install flask

WORKDIR /app

COPY app.py /app/
COPY run.sh /app/
COPY wsgi.py /app/
COPY psyducks /app/psyducks
COPY templates /app/templates
COPY supersecretbackup /app/supersecretbackup

WORKDIR /app

ENTRYPOINT ["./run.sh"]