#Download base image ubuntu 20.04
FROM ubuntu:20.04

LABEL version="0.1"
LABEL maintainer="chekalov.pavel@gmail.com"

RUN apt update && apt install -yqq software-properties-common && add-apt-repository ppa:deadsnakes/ppa && apt update && apt install -yqq python3 && apt install -yqq python3-venv && apt update
COPY ./src ./app/src
COPY ./tests ./app/tests
COPY ./setup.cfg ./app/setup.cfg
COPY ./.gitignore ./app/.gitignore
COPY ./req.txt ./app/req.txt
COPY ./Dockerfile ./app/Dockerfile
COPY ./.gitlab-ci.yml ./app/.gitlab-ci.yml
WORKDIR ./app
RUN python3 -m venv venv && . ./venv/bin/activate && apt-get install -yqq python3-pip && apt update
RUN pip3 install -r req.txt
#RUN python3 tests/append_paths.py
#RUN ['python3','src/app.py']
ARG host=127.0.0.1
ARG port=9999
ARG mpn=1000000000
ENV hostname=$host
ENV port_num=$port
ENV max_prime_num=$mpn
EXPOSE $port_num
CMD python3 src/web.py -H $hostname -p $port_num -mpn $max_prime_num
