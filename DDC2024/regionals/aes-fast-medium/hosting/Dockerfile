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
  chmod 740 /ctf/flag.txt && \
  pip3 install pycryptodome

RUN dos2unix /etc/xinetd.d/ctf && dos2unix /ctf/aesfast.py && dos2unix /ctf/chal.py && dos2unix /ctf/start.sh && dos2unix /ctf/flag.txt

ENTRYPOINT []
CMD ["/usr/sbin/xinetd", "-dontfork"]

EXPOSE 9999