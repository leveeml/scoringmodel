FROM python:3.7-stretch

RUN apt-get -y update && apt-get upgrade -y --no-install-recommends && \
  apt-get install -y --no-install-recommends \
  zip

WORKDIR /opt/server

RUN apt-get clean
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY src/ src
COPY resources/ resources
COPY conf.py .
COPY server.py .

CMD ["python","/opt/server/server.py"]
