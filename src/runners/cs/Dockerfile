FROM python:3.7-stretch
RUN apt-get update && \
    apt-get -y install mono-devel
COPY main.py /main.py
ENTRYPOINT ["python3", "main.py"]
