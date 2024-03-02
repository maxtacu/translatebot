FROM python:3.11

WORKDIR /usr/translatebot

COPY ./* /usr/translatebot/

RUN pip install -r requirements.txt

CMD [ "python", "./translatebot.py"]