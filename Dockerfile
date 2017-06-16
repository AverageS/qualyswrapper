FROM alpine
MAINTAINER Mikhail Aksenov <blabos@ya.ru>
RUN apk update
RUN apk add python3 py-pip
RUN pip3 install elasticsearch
COPY scanner.py /opt/ssl-scan/scanner.py
COPY ssllabs-scan /opt/ssl-scan/ssllabs-scan
CMD python3 /opt/ssl-scan/scanner.py