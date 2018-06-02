FROM python:2.7

MAINTAINER Mrinal Wahal / wahal.ga

ADD requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

ADD . /code
WORKDIR /code

EXPOSE 7777
EXPOSE 5000
    
CMD ["python", "app.py"]
