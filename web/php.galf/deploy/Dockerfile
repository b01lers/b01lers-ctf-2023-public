# We can build from whatever version
# we want. 20.04 is most typical now.

# FROM ubuntu:18.04
FROM php:7.4-apache

# Install any software needed to
# # build the challenge


# This assumes a C file but works perfectly OK
# with go/C++/rust, just install the right compiler
COPY src/exceptions/ /var/www/html/exceptions/
COPY src/keywords/ /var/www/html/keywords/
COPY src/parser/ /var/www/html/parser/
COPY solve/flag.php /var/www/html/
COPY src/index.php /var/www/html/
COPY src/php.ini /usr/local/etc/php/

# We don't want to forget the flag!


# COPY ./src/.htaccess var/www/html/
# COPY ./src/index.html var/www/html/


# Set permissions. Be *VERY* careful
# about changing this!
RUN chown -R root:$USER /home/$USER
RUN chmod -R 550 /home/$USER
RUN chmod -x /var/www/html/flag.php
EXPOSE 80