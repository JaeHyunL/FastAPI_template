FROM ubuntu:22.04

ENV PYTHONBUFFERED 1

RUN apt-get update && apt-get install -y \
    vim \
    net-tools \
    software-properties-common \
    wget \
    unzip \
    zip \
    locales \
    libxcb1 \
    libxcb1  \
    libfftw3-3 \
    python3.11


RUN apt-get update && \
    apt-get install -y python3.11 python3-pip

RUN pip3 install --upgrade pip
# RUN pip3 install -e .
# COPY ./requirements.txt /src/wiss/requirements.txt

# COPY . /src/wiss
# WORKDIR /src/wiss

