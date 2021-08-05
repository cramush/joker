FROM python:3.8

WORKDIR /api

ADD /requirements.txt ./requirements.txt

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

ADD . .

CMD ["python3", "api.py"]
