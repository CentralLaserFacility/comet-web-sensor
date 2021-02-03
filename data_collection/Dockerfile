FROM python:3.8-slim-buster

COPY . /src
WORKDIR /src

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "sensor_data.py"]
