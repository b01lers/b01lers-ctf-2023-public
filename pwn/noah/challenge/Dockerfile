FROM ubuntu:20.04 as ubuntu-build

RUN apt-get update && apt-get install -y build-essential gcc make

COPY Makefile /
COPY chal.c /
COPY constants.h /
COPY mem.S /
COPY mem.h /
COPY readint.c /
RUN make noah readint

FROM ubuntu:20.04 as chroot

COPY flag.txt /
COPY golf_flag.txt /
COPY --from=ubuntu-build noah /
COPY --from=ubuntu-build readint /
COPY wrapper.sh /

RUN chmod +x wrapper.sh

FROM gcr.io/kctf-docker/challenge@sha256:d884e54146b71baf91603d5b73e563eaffc5a42d494b1e32341a5f76363060fb

COPY --from=chroot / /chroot

COPY nsjail.cfg /home/user/

CMD kctf_setup && \
    kctf_drop_privs \
    socat \
      TCP-LISTEN:1337,reuseaddr,fork \
      EXEC:"kctf_pow nsjail --config /home/user/nsjail.cfg -- /wrapper.sh"
