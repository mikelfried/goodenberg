FROM ubuntu:23.04

ENV DEBIAN_FRONTEND noninteractive

# RUN apt-get update && apt-get -y upgrade && \
#     apt-get -y install python3.10 && \
#     apt update && apt install python3-pip -y

RUN apt-get update && apt-get -y install python3.10 python3-pip

RUN apt-get --no-install-recommends install libreoffice -y
RUN apt-get install -y libreoffice-java-common

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN echo "@daily root find /tmp/* -atime +1 -type f -delete" >> /etc/crotab

COPY main.py /main.py

CMD ["/bin/bash", "-c", "unoserver & uvicorn --host 0.0.0.0 --port 80 main:app"]
