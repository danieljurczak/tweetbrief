FROM ubuntu:18.04

ENV LANG C.UTF-8
RUN apt-get update && apt-get -y install build-essential python python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info fonts-noto-color-emoji cron nano

RUN mkdir /code
WORKDIR /code

COPY cron-job /etc/cron.d/cron-job
RUN chmod 0644 /etc/cron.d/cron-job
RUN crontab /etc/cron.d/cron-job
RUN touch /var/log/cron.log
CMD cron && tail -f /var/log/cron.log

COPY requirements.txt /code/
RUN pip3 install -r requirements.txt
COPY . /code/
RUN chmod 0744 /code/cron.sh
RUN chmod 777 -R /code
