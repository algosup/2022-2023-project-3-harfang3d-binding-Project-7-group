# FROM python:3
FROM ubuntu:latest

WORKDIR /usr/src/tests

COPY requirements.txt /usr/src/tests

RUN apt update -y && apt upgrade -y

RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install --no-cache-dir -r requirements.txt

RUN apt-get install -y lua5.3

RUN apt-get install -y golang-go
RUN apt-get install -y golang-golang-x-tools

RUN apt-get install -y xdg-utils

RUN apt-get install -y cargo

RUN apt-get install -y clang-format

RUN apt-get install -y cmake
# python3 tests.py --linux --rust --debug arg_out    