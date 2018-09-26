FROM python:3.7-stretch
RUN apt-get update && apt-get -y install openjdk-8-jdk
COPY main.py /main.py
ENTRYPOINT ["python3", "main.py"]
