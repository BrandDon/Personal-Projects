FROM python:3.6-alpine

COPY . /pastebin_crawler
WORKDIR /pastebin_crawler


RUN pip install -r requierments.txt
WORKDIR /pastebin_crawler/pastebin_crawler

ENV PYTHONPATH=/pastebin_crawler
ENTRYPOINT python main.py