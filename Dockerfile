FROM ubuntu
MAINTAINER Mikhail Aksenov <blabos@ya.ru>
RUN apt-get update
RUN apt-get install -y python3-pip
RUN pip3 install elasticsearch
COPY scanner.py /opt/ssl-scan/scanner.py
COPY ssllabs-scan /opt/ssl-scan/ssllabs-scan
CMD python3 /opt/ssl-scan/scanner.py