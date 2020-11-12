FROM python:3.8
ENV PYTHONUNBUFFERED 1
# from https://rtfm.co.ua/en/docker-configure-tzdata-and-timezone-during-build/
ENV TZ=Etc/UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
  echo $TZ > /etc/timezone

RUN apt-get update \
  && apt-get install -y php php-gmp

RUN mkdir /code
RUN mkdir /code/lib
RUN git clone https://github.com/DeckerSU/BitcoinECDSA.php.git /code/BitcoinECDSA.php && \
  cd code/BitcoinECDSA.php && \
  git checkout b4b0ca4
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY run.sh /code
COPY genaddressonly.php /code
COPY genwallet.php /code
COPY new_org_wallet /code
COPY lib/transaction.py /code/lib
COPY lib/bitcoin.py /code/lib
COPY lib/util.py /code/lib
COPY lib/i18n.py /code/lib
COPY lib/version.py /code/lib
COPY lib/constants.py /code/lib
COPY lib/keystore.py /code/lib
COPY lib/mnemonic.py /code/lib
COPY lib/plugins.py /code/lib
COPY lib/rpclib.py /code/lib
COPY lib/juicychain.py /code/lib
COPY lib/juicychain_env.py /code/lib
# COPY .env /code
COPY run.py /code
WORKDIR /code

#COPY ./ /code/
