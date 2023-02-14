FROM ubuntu:22.04

RUN apt update

RUN apt install -y vim less make python3 python3-pip
RUN pip3.10 install robotframework
RUN pip3.10 install antlr4

