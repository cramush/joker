FROM python:3.8

WORKDIR /api

RUN mkdir /etc/joker_api/

ADD /secrets.yaml ./etc/joker_api/secrets.yaml

ADD /requirements.txt ./requirements.txt

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

ADD . .

CMD ["python3", "api.py"]
