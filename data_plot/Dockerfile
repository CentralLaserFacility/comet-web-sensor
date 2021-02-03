FROM python:3.8-slim-buster

COPY . /src

WORKDIR /src

# dependencies
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "server-ui.py"]
