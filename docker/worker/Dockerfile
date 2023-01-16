FROM python:3.9-buster

COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

COPY ./app /app
COPY ./*.sh /
WORKDIR /app
ENTRYPOINT ["/entrypoint.sh"]
