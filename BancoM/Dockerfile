FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install Pyro5 pymongo schedule

CMD ["python3", "server.py"]