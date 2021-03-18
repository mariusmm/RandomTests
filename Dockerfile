FROM python:3.6 as base

ENV CWS=/home/tracker/app \
    VENV=/home/tracker/env

WORKDIR /tmp

COPY ./requirements.txt .

RUN useradd tracker && \
    python3 -m venv ${VENV} && \
    ${VENV}/bin/pip install --upgrade pip setuptools && \
    ${VENV}/bin/pip install -r requirements.txt && \
    rm /tmp/* -R 

FROM base as install-pyramid

WORKDIR /home/tracker

COPY app ${CWS}
COPY development.ini .
COPY setup.py .

RUN ${VENV}/bin/pip install -e . 

CMD ["sh", "-c", "$VENV/bin/pserve development.ini --reload"]

# Exposed pyramid port
EXPOSE 10000
