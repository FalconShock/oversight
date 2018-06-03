FROM python:2.7

MAINTAINER Mrinal Wahal / wahal.ga

ADD requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

ADD . /code
WORKDIR /code

EXPOSE 80:80
EXPOSE 3306:3306

CMD ["python", "app.py"]
