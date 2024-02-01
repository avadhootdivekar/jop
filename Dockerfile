FROM ubuntu:22.04

RUN apt-get update && \
        apt-get install -y vim less make python3 python3-pip git antlr4 patchelf&& \
        python3 -m pip install robotframework && \
        python3 -m pip install antlr4-python3-runtime && \
        python3 -m pip install antlr4-grun && \
        python3 -m pip install numpy && \
        python3 -m pip install nuitka;
