# Raspberry Pi
#FROM arm32v6/python:alpine3.6

# Raspberry Pi 2/3
# FROM arm32v7/python

# All pi?
#FROM resin/raspberry-pi-alpine-python:3.6.1-onbuild
FROM hypriot/rpi-alpine

MAINTAINER Chris Diehl <cultclassik@gmail.com>

ENV INITSYSTEM on

RUN apk update && apk add \
    bash fping \
    git \
    python-dev

RUN git clone https://github.com/CultClassik/rpilo.git /rpilo

EXPOSE 5000

CMD ["python /rpilo/rpilo.py"]

# Example usage:
# docker run -d --name raspi-powerctl -p 5000:5000 --cap-add SYS_RAWIO --device /dev/mem cultclassik/raspi-powerctl
# docker run --name raspi-powerctl -p 5000:5000 --cap-add SYS_RAWIO --device /dev/mem cultclassik/raspi-powerctl