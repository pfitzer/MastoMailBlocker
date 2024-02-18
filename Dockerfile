FROM python:3.11-alpine

RUN mkdir /code
WORKDIR /code

COPY . /code
COPY .crontab/app-cronjob.sh /etc/periodic/weekly/app-cronjob.sh

RUN chmod +x /etc/periodic/weekly/app-cronjob.sh

# uwsgi setup
RUN apk add python3-dev build-base linux-headers pcre-dev
RUN pip install uwsgi
RUN pip install -r requirements.txt

EXPOSE 3031

CMD ["uwsgi", "--ini", "/code/mastomailblocker.uwsgi.ini"]