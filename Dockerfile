FROM python:3.6-slim
WORKDIR /project
ADD . /project
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python", "server2.py"]