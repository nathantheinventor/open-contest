FROM python:3.8-stretch
RUN apt-get update && apt-get -y install openjdk-11-jdk
COPY main.py /main.py
ENTRYPOINT ["python3", "main.py"]
