FROM python:3.6.1-alpine

RUN apk update
RUN apk add --no-cache gcc git python3-dev musl-dev postgresql-dev

WORKDIR /code

RUN pip install --upgrade pip
ADD requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

ADD . /code/

VOLUME '/static'

EXPOSE 8000

CMD ["/bin/sh", "bootstrap.sh"]
