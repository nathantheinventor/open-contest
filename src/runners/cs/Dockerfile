FROM python:3.7-stretch
RUN apt-get update && \
    apt-get -y install apt-transport-https dirmngr && \
    apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF && \
    echo "deb https://download.mono-project.com/repo/debian stable-stretch main" | tee /etc/apt/sources.list.d/mono-official-stable.list && \
    apt-get update && \
    apt-get -y install mono-devel
COPY main.py /main.py
ENTRYPOINT ["python3", "main.py"]
