# Ubuntu 18.04 LTS base image with supervisord and an extensible Python based startup system

[![Build Status](https://travis-ci.com/GriffinPlus/docker-base-supervisor.svg?branch=master)](https://travis-ci.com/GriffinPlus/docker-base-supervisor)
[![Docker Pulls](https://img.shields.io/docker/pulls/griffinplus/base-supervisor.svg)](https://hub.docker.com/r/griffinplus/base-supervisor/)
[![Github Stars](https://img.shields.io/github/stars/griffinplus/docker-base-supervisor.svg?label=github%20%E2%98%85)](https://github.com/griffinplus/docker-base-supervisor/)
[![Github Stars](https://img.shields.io/github/contributors/griffinplus/docker-base-supervisor.svg)](https://github.com/griffinplus/docker-base-supervisor/)
[![Github Forks](https://img.shields.io/github/forks/griffinplus/docker-base-supervisor.svg?label=github%20forks)](https://github.com/griffinplus/docker-base-supervisor/)

## Overview

This is a Docker base image built on top of the Griffin+ base image. In addition to the *Griffin+ Container Startup System* shipped with the base image, this image comes with [supervisord](http://supervisord.org) to run custom services added in derived images. For more information about the startup system, please see the documentation of the [Griffin+ base image](https://github.com/GriffinPlus/docker-base).

## For Developers

### Creating a Custom Image based on this Image

The image is quite simple to use, since there is an [automated build](https://hub.docker.com/r/griffinplus/base-supervisor) on [Docker Hub](https://hub.docker.com). Just add the following line at the beginning of your `Dockerfile`:

```
FROM griffinplus/base-supervisor
```

### Adding a Service to Start

To let *supervisord* start a custom service, you only need to place a service configuration file (*.conf) for *supervisord* in `/etc/supervisor/conf.d/`. The service must have the following characteristics:
- The service must run in foreground mode.
- The process should honor the TERM signal and shut down gracefully (the signal can be overridden using the `stopsignal` setting, see [documentation](http://supervisord.org/configuration.html#program-x-section-settings)).

The following simple example will spawn NGINX.

```
# /etc/supervisor/conf.d/nginx.conf
[program:nginx]
command=/usr/sbin/nginx -g "daemon off;"
```

See the documentation of [supervisord](http://supervisord.org) for details on how to adjust supervisord settings according to your needs.
