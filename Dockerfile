FROM ubuntu:22.04

RUN apt-get update

RUN apt-get install -y vim less make python3 python3-pip git antlr4
RUN python3 -m pip install robotframework
RUN python3 -m pip install antlr4-python3-runtime
RUN python3 -m pip install antlr4-grun
RUN python3 -m pip install numpy
