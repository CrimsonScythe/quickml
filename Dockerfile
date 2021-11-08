FROM python:3.6-slim
ADD . /quickml
WORKDIR /quickml
RUN pip install -r requirements.txt
WORKDIR /quickml/app/main