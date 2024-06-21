FROM sagemath/sagemath:10.3

USER root

RUN apt-get -qq update \
    && apt-get -qq install -y --no-install-recommends \
    netcat \
    tmux \
    vim \
    xinetd \
    python3 \
    python3-pip \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /ctf
WORKDIR /ctf

RUN echo "Connection blocked" > /etc/banner_fail
COPY ./src/ctf.xinetd /etc/xinetd.d/ctf
COPY ./src/*.sage /ctf/
COPY ./src/flag.txt /ctf/
COPY ./src/init.sh /ctf/

RUN chmod -R 750 /ctf && \
  chmod 740 /ctf/flag.txt

RUN dos2unix /etc/xinetd.d/ctf && dos2unix /ctf/*.sage && dos2unix /ctf/init.sh && dos2unix /ctf/flag.txt

ENTRYPOINT []
EXPOSE 1337
CMD ["/usr/sbin/xinetd", "-dontfork"]