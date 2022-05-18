FROM python:3.9.12

WORKDIR /usr/translatebot

COPY ./* /usr/translatebot/

RUN pip install -r requirements.txt

CMD [ "python", "./translatebot.py"]