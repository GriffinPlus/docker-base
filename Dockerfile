FROM ubuntu:18.04
MAINTAINER Sascha Falk <sascha@falk-online.eu>

# update image and install additional packages
ENV DEBIAN_FRONTEND=noninteractive
RUN \
  apt-get -y update && \
  apt-get -y install \
    git \
    lsb-release \
    python3 \
    python3-chardet \
    python3-dnspython \
    python3-mako \
    python3-netaddr \
    python3-netifaces \
    python3-openssl && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

# copy prepared files into the image
COPY target /

# adjust permissions
RUN \
  chmod 750 /docker-entrypoint.sh && \
  chmod 750 /docker-startup/run-startup.sh

# add starting the application to .bashrc of root to support the 'run-and-enter' mode
# and let it terminate before the opened shell exits
RUN \
  echo 'if [[ "${RUN_DOCKER_APP}" -eq "1" ]]; then' >> /root/.bashrc && \
  echo '  /docker-startup/run-app.sh > /var/log/app-stdout.log 2> /var/log/app-stderr.log &' >> /root/.bashrc && \
  echo '  export DOCKER_APP_PID=$!' >> /root/.bashrc && \
  echo '  trap "kill ${DOCKER_APP_PID}" EXIT' >> /root/.bashrc && \
  echo '  echo "The application was started, its stdout/stderr is logged to /var/log/app-[stdout|stderr].log."' >> /root/.bashrc && \
  echo 'fi' >> /root/.bashrc

# configure container startup
ENTRYPOINT [ "/docker-entrypoint.sh" ]
CMD [ "run" ]
