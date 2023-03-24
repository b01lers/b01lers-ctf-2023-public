# We can build from whatever version
# we want. 20.04 is most typical now.

FROM python:3

# Install any software needed to
# build the challenge

RUN apt-get update && apt-get install -y xinetd
RUN apt-get update && apt-get install -y qemu-system-x86
RUN apt-get update && apt-get install -y socat

# Change example to the name of your challenge.

ENV USER knock_knock
WORKDIR /home/$USER
RUN useradd $USER

# This adds the critical files.

# wrapper.sh wraps the executable by 
# `cd`ing to the right place

COPY ./deploy/wrapper.sh /home/$USER/

# The xinetd configuration provides run options
# but is very boilerplate. See below. 
COPY ./deploy/xinetd.conf /etc/xinetd.d/$USER

COPY ./src/chall.py /home/$USER/
COPY ./src/disk_final.img /home/$USER/

# Set permissions. Be *VERY* careful
# about changing this!
RUN chown -R root:$USER /home/$USER
RUN chmod -R 550 /home/$USER
RUN touch /var/log/xinetdlog

# Whatever port you configured in xinetd.
# PROBABLY this should stay 1337. Just change
# The passthrough port in docker-compose.yml below.
EXPOSE 1337

# Start the container by starting xinetd and outputting
# the xinetd log for debugging.
CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"python /home/$USER/chall.py"
