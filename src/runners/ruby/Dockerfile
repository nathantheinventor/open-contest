FROM python:3.7
RUN apt-get update && \
    apt-get -y install ruby
COPY main.py /main.py
ENTRYPOINT ["python3", "main.py"]