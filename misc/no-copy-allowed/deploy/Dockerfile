FROM alpine

RUN apk update \
    && apk add lighttpd python3 python3-dev gcc g++ make \
    && rm -rf /var/cache/apk/*

RUN python3 -m ensurepip
RUN pip3 install fontmake
RUN mkdir chall_gen

WORKDIR /chall_gen

COPY ./src/fonts ./fonts
COPY ./src/gen.py ./
RUN python3 gen.py

CMD ["lighttpd","-D","-f","/etc/lighttpd/lighttpd.conf"]
