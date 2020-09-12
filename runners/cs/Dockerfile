FROM mono:latest

RUN apt-get update && apt-get install -y python3
COPY main.py /main.py
ENTRYPOINT ["python3", "main.py"]
