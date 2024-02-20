FROM python:3.11-alpine

RUN mkdir /code
WORKDIR /code

COPY . /code

# uwsgi setup
RUN apk add python3-dev build-base linux-headers pcre-dev
RUN pip install uwsgi
RUN pip install supervisor
RUN pip install -r requirements.txt

EXPOSE 3031

CMD ["uwsgi", "--ini", "/code/uwsgi.docker.ini"]