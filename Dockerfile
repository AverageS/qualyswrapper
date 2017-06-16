FROM alpine
MAINTAINER Mikhail Aksenov <blabos@ya.ru>
RUN apk update
RUN apk add python py-pip
RUN pip install elasticsearch
RUN apk add wget
RUN pip install elasticsearch
COPY scanner.py /opt/ssl-scan/scanner.py
COPY ssllabs-scan /opt/ssl-scan/ssllabs-scan
CMD python3 /opt/ssl-scan/scanner.py