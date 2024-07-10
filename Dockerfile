FROM python:3.9.0-alpine

RUN apk update 

# you can specify python version during image build
ARG PYTHON_VERSION=3.10.0

# install build dependencies and needed tools
RUN apk add \
    wget \
    curl \
    gcc \
    make \
    zlib-dev \
    libffi-dev \
    openssl-dev \
    musl-dev  

COPY ./src/requirements.txt /requirements.txt 
RUN  pip install --upgrade pip
RUN pip install -r /requirements.txt

COPY ./entrypoint.sh /entrypoint.sh

ENV ES_PASS=${ES_PASS}
ENV OPENAI_API_KEY=${OPENAI_API_KEY}


ENTRYPOINT ["./entrypoint.sh"]
