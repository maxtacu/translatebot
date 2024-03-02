FROM python:3.11.8-alpine3.18

WORKDIR /usr/translatebot

COPY ./* /usr/translatebot/

RUN pip install -r requirements.txt

CMD [ "python", "./translatebot.py"]