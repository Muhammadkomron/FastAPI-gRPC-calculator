FROM python:3.11-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY ./protobuf ./protobuf

RUN python -m grpc_tools.protoc -I ./protobuf --python_out=. --grpc_python_out=. calculator.proto

COPY . .