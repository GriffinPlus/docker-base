FROM griffinplus/base
MAINTAINER Sascha Falk <sascha@falk-online.eu>

# install additional packages
RUN \
  apt-get -y update && \
  apt-get -y install supervisor && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

# copy prepared files into the image
COPY target /
