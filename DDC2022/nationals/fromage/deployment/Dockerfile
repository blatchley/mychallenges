FROM ubuntu:20.04

RUN apt-get update && apt-get install -y \
  xinetd \
  python3 \
  python3-pip \
  dos2unix \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir /ctf
WORKDIR /ctf
RUN useradd -M -d /ctf ctf

RUN echo "Connection blocked" > /etc/banner_fail
COPY ctf.xinetd /etc/xinetd.d/ctf
COPY ./src /ctf/

RUN chown -R root:ctf /ctf && \
  chmod -R 750 /ctf && \
  chmod 740 /ctf/drapeau.txt && \
  pip3 install pycryptodome && \
  pip3 install gmpy2

RUN dos2unix /etc/xinetd.d/ctf && dos2unix /ctf/challenge.py && dos2unix /ctf/drapeau.txt  && dos2unix /ctf/start.sh 


ENTRYPOINT []
CMD ["/usr/sbin/xinetd", "-dontfork"]

EXPOSE 9999