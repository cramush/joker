FROM python:3.8

WORKDIR /bot

RUN mkdir /etc/joker_bot/

ADD secrets.yaml /etc/joker_bot/secrets.yaml

ADD /requirements.txt ./requirements.txt

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

ADD . .

CMD ["python3", "bot.py"]
