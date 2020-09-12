FROM python:3.8-buster
RUN apt-get update 
RUN apt-get install -y ruby

COPY main.py /main.py
ENTRYPOINT ["python3", "main.py"]
