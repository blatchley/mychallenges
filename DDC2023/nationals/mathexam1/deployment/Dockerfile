FROM sagemath/sagemath:9.6

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
COPY ctf.xinetd /etc/xinetd.d/ctf
COPY ./src /ctf/

RUN chmod -R 750 /ctf && \
  pip3 install pycryptodome 

RUN dos2unix /etc/xinetd.d/ctf && dos2unix /ctf/challenge.py && dos2unix /ctf/start.sh && dos2unix /ctf/secretdata.py

ENTRYPOINT []
CMD ["/usr/sbin/xinetd", "-dontfork"]

EXPOSE 9999