FROM python:3.8
ENV PYTHONUNBUFFERED 1
# from https://rtfm.co.ua/en/docker-configure-tzdata-and-timezone-during-build/
ENV TZ=Etc/UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
  echo $TZ > /etc/timezone

RUN apt-get update \
  && apt-get install -y php php-gmp

COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN mkdir /code
RUN mkdir /code/lib
COPY run.sh /code
COPY test.py /code
COPY genaddressonly.php /code
COPY lib/rpclib.py /code/lib
COPY .env /code
# COPY BitcoinECDSA.php /code/BitcoinECDSA.php
RUN git clone https://github.com/DeckerSU/BitcoinECDSA.php.git /code/BitcoinECDSA.php && \
  cd code/BitcoinECDSA.php && \
  git checkout b4b0ca4
WORKDIR /code

#COPY ./ /code/
