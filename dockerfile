FROM python:3.11.1

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip install -r /usr/src/app/requirements.txt

RUN rm -rf /usr/src/app

COPY . /usr/src/app

CMD [ "python3", "./main.py"]