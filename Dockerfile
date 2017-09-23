# Raspberry Pi
#FROM arm32v6/python:alpine3.6

# Raspberry Pi 2/3
# FROM arm32v7/python

# All pi?
#FROM resin/raspberry-pi-alpine-python:3.6.1-onbuild
FROM hypriot/rpi-alpine

MAINTAINER Chris Diehl <cultclassik@gmail.com>

ENV INITSYSTEM on

RUN apk update && apk add --no-cache \
    bash fping git gcc musl-dev linux-headers python3 python3-dev

RUN python3 -m ensurepip &&\
    rm -r /usr/lib/python*/ensurepip &&\
    pip3 install --upgrade pip

RUN git clone https://github.com/CultClassik/rpilo.git /rpilo

WORKDIR /rpilo

RUN pip3 install -r /rpilo/requirements.txt

EXPOSE 5000

CMD ["python3", "/rpilo/rpilo.py"]
