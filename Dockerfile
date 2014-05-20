FROM ubuntu
MAINTAINER Danny Berger <dpb587@gmail.com>

RUN ( nc -zw 8 172.17.42.1 3142 && echo 'Acquire::http { Proxy "http://172.17.42.1:3142"; };' > /etc/apt/apt.conf.d/01proxy ) || true

ADD . /docker

WORKDIR /docker

RUN [ "./bin/install.sh" ]

ENTRYPOINT [ "./bin/run.py" ]
