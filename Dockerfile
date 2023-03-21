FROM ubuntu:23.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get -y install python3.10 python3-pip

RUN apt-get --no-install-recommends install libreoffice -y
RUN apt-get install -y libreoffice-java-common

RUN pip3 install --break-system-packages unoserver && pip3 install --break-system-packages fastapi uvicorn python-multipart

RUN echo "@daily root find /tmp/* -atime +1 -type f -delete" >> /etc/crotab

COPY main.py /main.py

CMD ["/bin/bash", "-c", "unoserver & uvicorn --host 0.0.0.0 --port 80 main:app"]
