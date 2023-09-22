FROM ubuntu:16.04

RUN apt-get update -y && apt-get install -y \
    lib32z1 xinetd \
    dos2unix \
    build-essential

RUN useradd -m ctf

WORKDIR /home/ctf

RUN cp -R /lib* /home/ctf && \
    cp -R /usr/lib* /home/ctf

RUN mkdir /home/ctf/dev && \
    mknod /home/ctf/dev/null c 1 3 && \
    mknod /home/ctf/dev/zero c 1 5 && \
    mknod /home/ctf/dev/random c 1 8 && \
    mknod /home/ctf/dev/urandom c 1 9 && \
    chmod 666 /home/ctf/dev/*

RUN mkdir /home/ctf/bin && \
    cp /bin/sh /home/ctf/bin && \
    cp /bin/ls /home/ctf/bin && \
    cp /bin/cat /home/ctf/bin

COPY ./ctf.xinetd /etc/xinetd.d/ctf
COPY ./start.sh /start.sh
COPY ./bin/ /home/ctf/

RUN dos2unix /etc/xinetd.d/ctf && dos2unix /start.sh && dos2unix /home/ctf/flag.txt && dos2unix /home/ctf/Makefile && dos2unix /home/ctf/pwd.c && dos2unix /home/ctf/mix.cc && dos2unix /home/ctf/start.sh

RUN make kidz

RUN echo "Blocked by ctf_xinetd" > /etc/banner_fail

RUN chmod +x /start.sh

RUN chown -R root:ctf /home/ctf && \
    chmod -R 750 /home/ctf 

CMD ["/start.sh"]

EXPOSE 9999