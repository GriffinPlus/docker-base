# Ubuntu 18.04 LTS base image with an extensible Python based startup system

[![Build Status](https://travis-ci.com/GriffinPlus/docker-base.svg?branch=master)](https://travis-ci.com/GriffinPlus/docker-base)
[![Docker Pulls](https://img.shields.io/docker/pulls/griffinplus/base.svg)](https://hub.docker.com/r/griffinplus/base/)
[![Github Stars](https://img.shields.io/github/stars/griffinplus/docker-base.svg?label=github%20%E2%98%85)](https://github.com/griffinplus/docker-base/)
[![Github Stars](https://img.shields.io/github/contributors/griffinplus/docker-base.svg)](https://github.com/griffinplus/docker-base/)
[![Github Forks](https://img.shields.io/github/forks/griffinplus/docker-base.svg?label=github%20forks)](https://github.com/griffinplus/docker-base/)

## Overview

This is a Docker base image based on Ubuntu 18.04 LTS and comes with a startup system based on Python 3 that is run when the container starts up.

## Environment Variables

#### STARTUP_VERBOSITY

The *Griffin+ Container Startup System* (see below for details) contains a simple logging system with five log levels (error, warning, note, info, debug) messages can be associated with. The environment variable `STARTUP_VERBOSITY` determines the maximum log level a message can  have to get into the log:

- 0 => Logging is disabled.
- 1 => Only errors are logged.
- 2 => Errors and warnings are logged.
- 3 => Errors, warnings and notes are logged.
- 4 => Errors, warnings, notes and infos are logged.
- 5 => All messages are logged.

Default: `4`

## For Users (of derived Images)

The startup system described below supports the commands `run` (default) and `run-and-enter` that lets the container start up and run the shipped service, optionally opening an interactive shell (bash) in the container. This is primarily useful for debugging purposes.

```
# start service shipped in the container...
docker run griffinplus/base run

# ...or simply ('run' is used by default)
docker run griffinplus/base
```

## For Developers

### Creating a Custom Image based on this Image

The image is quite simple to use, since there is an [automated build](http://hub.docker.com/r/griffinplus/base) on [Docker Hub](http://hub.docker.com). Just add the following line at the beginning of your `Dockerfile`:

```
FROM griffinplus/base
```

### Adding Code to Run at Startup
There are two locations where custom startup code can be placed - one for generic scripts/applications and one for the Python-based *Griffin+ Container Startup System*.

#### Generic Scripts
Any script/application at `/docker-startup/*.startup/startup` is run in ascending alphabetical order. The *Griffin+ Container Startup System* (at `/docker-startup/10-initial.startup/startup`) is started this way as well. The startup code makes the `startup` scripts executable, so there is no need to take care of it in derived images.

#### Griffin+ Container Startup System

The *Griffin+ Container Startup System* is a framework to build startup scripts with the power of Python 3. It eases writing startup code by bringing along common functionality like logging, environment variable evaluation, network interface handling and so on.

One purpose of custom startup code is the handling of commands controlling the container's behavior. Many containers only have rudimentary support for custom commands that allow the execution of programs via `docker run` only. The *Griffin+ Container Startup System* lets you implement *command processor plugins* that are called, if you specify certain parameters with the `docker run` call. All containers support the commands `run` to simply run the container and `run-and-enter` to start the container and open a shell in it. This can be very handy when debugging containers.

##### Installed Python 3 Packages

The image contains the following Python packages that can be used within the plugins:
- [chardet](https://chardet.readthedocs.io)
- [dnspython](http://www.dnspython.org/)
- [mako](http://www.makotemplates.org/)
- [netaddr](https://netaddr.readthedocs.io/)
- [netifaces](https://bitbucket.org/al45tair/netifaces)
- [openssl](https://pyopenssl.readthedocs.io)

##### Logging

The logging system supports logging to stdout/stderr, file and syslog depending on the use case. If the container is started with the command `run` or `run-and-enter` messages are logged to stdio and to file or syslog. Logging to syslog is chosen, if `/dev/log` is mounted into the container. Any message written to syslog is associated with facility *local5* by default. If syslog is not available, messages are logged to file (`/var/log/gp_startup.log`) instead. If the container is started with some custom command (i.e. *not* `run` or `run-and-enter`), logging to stdio is disabled to avoid mixing up logged messages and text that needs to be consumed by the caller.

The logging system is implemented in the `gp_log` module. It contains the `Log` class and a few static methods to write formatted messages of different severity levels to the log:
```
- Log.write_error(format, *args)   : Level 1, writes to stderr / syslog priority Error (3)
- Log.write_warning(format, *args) : Level 2, writes to stdout / syslog priority Warning (4)
- Log.write_note(format, *args)    : Level 3, writes to stdout / syslog priority Note (5)
- Log.write_info(format, *args)    : Level 4, writes to stdout / syslog priority Informational (6)
- Log.write_debug(format, *args)   : Level 5, writes to stdout / syslog priority Debug (7)
```

The `Log.set_verbosity(level)` method sets the verbosity of the log. Setting the verbosity to level `5` (or greater) lets you see all messages written to the log. The default is level `4`, so only messages concerning errors, warnings, notes and infos are shown while debug messages are suppressed. This method should not be used, since it interferes with the handling of the `STARTUP_VERBOSITY` environment variable. It's recommended to use the environment variable to influence the verbosity instead of changing the verbosity programmatically on your own.

##### Helper Functions

The *Griffin+ Container Startup System* is shipped with some helper functions that ease writing the plugins by providing common functionality. The helper functions are implemented in the `gp_helpers` module. The following functions are provided:
- accessing environment variables
  - `get_env_setting_bool(var_name, default_value = None)`
  - `get_env_setting_integer(var_name, default_value = None, min = None, max = None)`
  - `get_env_setting_string(var_name, default_value = None)`
- console/terminal operations
  - `print_error(message, *args)`
  - `readline_if_no_tty`
- filesystem operations
  - `copy_directory(src_path, dest_path)`
  - `read_text_file(filename, encoding = None)`
  - `remove_tree(path)`
  - `touch_file(path)`
  - `write_text_file(filename, encoding, text)`
- handling configuration files
  - `replace_php_define(text, variable, value)`
  - `replace_php_variable(text, variable, value)`
- handling kernel modules
  - `is_kernel_module_loaded(module_name)`
  - `load_kernel_module(module_name)`
- handling mount points
  - `does_mount_point_exist(mount_point)`
  - `is_mount_point_readonly(mount_point)`
- networking
  - `is_email_address(s)`
  - `iptables_add(table, target, args=[], comment=None)`
  - `iptables_run(args, comment=None)`
  - `ip6tables_add(table, target, args=[], comment=None)`
  - `ip6tables_run(args, comment=None)`
  - `resolve_hostname(hostname)`
  - `resolve_hostnames(hostnames)`
- other stuff
  - `generate_password(length, chars = '...')`

##### Command Processor Plugins

Essentially a command processor plugin contains a class that derives from the `CommandProcessor` class (part of the framework, module *gp_cmdproc*) and overrides a method adding its own command handling code. The command processor plugins are deployed in `/docker-startup/10-initial.startup/gp_startup/plugins/`. The name of a plugin file must follow the `gp_cmdproc_*.py` pattern to be recognized by the plugin factory.

Command processor plugins are loaded and executed by file name in ascending alphabetical order by invoking the `CommandProcessor.process()` method of a plugin. This method must return an exit code, if the command was handled. If exit code `0` is returned, other command processor plugins are called as well. This enables writing startup code that is deployed using multiple plugins. If a command processor plugin returns a code that is not `0` other command processor plugins are skipped and the startup system exits gracefully with that exit code. If no command processor was able to handle the specified command, the startup system exits with error 127 (common shell error code for 'command not found').

The `CommandProcessor` class brings along a nice default implementation. You can register command handlers for different commands and bind functions to these commands, so the appropriate handler is called for a certain set of command line arguments. Furthermore you can specify, which *positional arguments* and *named arguments* the command expects/supports. An argument that starts with `--` is considered a *named argument*. The *named argument* may contain a `=` splitting the argument's name and its value. Named arguments may occur multiple times. If the `=` is missing, the *named argument* is still considered existent, but it has a `None` value. Any other arguments are considered *positional arguments* that are passed to the handler in the order they are specified.

The default implementation of `CommandProcessor.process()` conditions the command line arguments and splits them up into *positional arguments* and *named arguments*. When it comes to selecting which registered handler is to invoke, the handler with the most matching *positional arguments* is taken. *Named arguments* do not influence the selection. This eases writing command processing plugins, because the framework knows which command processor (respectively handler) is responsible for a specified command.

###### Command Handler Methods

A command handler method must return an integer value that becomes the return value of `CommandProcessor.process()`. If the return value of `CommandProcessor.process()` is `None` (no appropriate command handler was found) or `0` (the command handler completed successfully) other command processor plugins are called. Processing is aborted, if a handler and therefore `CommandProcessor.process()` returns with some other code. This code becomes the exit code of the startup system and is in turn returned from the docker container. An alternative way of setting an error code is raising an exception that derives from the `ExitCodeError` class (module *gp_errors*). The following exception classes are already defined in this module:

| Exception                   | Exit Code  | Description                                                         |
| :-------------------------- | :--------: | :------------------------------------------------------------------ |
| `GeneralError`              |     1      | An error that was not specified any further occurred.               |
| `CommandLineArgumentError`  |     2      | There is something wrong with the specified command line arguments. |
| `FileNotFoundError`         |     3      | A file needed for the requested operation does not exist.           |
| `IoError`                   |     4      | An I/O operation failed.                                            |
| `ConfigurationError`        |     5      | There is something wrong with the configuration of the container.   |

If any of these exceptions is raised in a command handler, the exception is caught, the associated error message is printed to *stderr* and its exit code is used as if the command handler had simply returned the code. Custom exception classes can benefit from the system by deriving from the `ExitCodeError` class as well.

Any other exception class not deriving from `ExitCodeError` can be configured to be mapped to an exit code as well by registering the exception type and a handler that maps the exception object to an exit code using `CommandProcessor.add_exception_handler(handler, exception_type)`. A registered handler takes the exception object as argument and returns the desired exit code to use instead.

Handler methods that are invoked when a certain set of positional arguments is specified in the command line can be registered using 
`CommandProcessor.add_handler(handler, *args)`.
The arguments are instances of the `PositionalArgument` class or the `NamedArgument` class.

Positional arguments are defined by the name they are expected to have in the command line.
```
PositionalArgument(name)
```

Named arguments are defined by the name they are expected to have in the command line following two hyphens (`--`). Furthermore a named argument can be configured to be read from *stdin* by setting `from_stdin = True`. The parameters `min_occurrence` and `max_occurrence` specify how often a named argument is expected to be specified in the command line. If `from_stdin = True` the framework will try to read `max_occurrence` lines from *stdin*. By default a named argument is not read from *stdin* and occurs only once or not at all.
```
NamedArgument(name, from_stdin = False, min_occurrence = 0, max_occurrence = 1)
```

###### Example

A simple command processor plugin looks like this:

```
# /docker-startup/10-initial.startup/gp_startup/plugins/gp_cmdproc_sample.py

import os

from ..gp_log import Log
from ..gp_cmdproc import CommandProcessor, PositionalArgument, NamedArgument
from ..gp_errors import GeneralError, CommandLineArgumentError, FileNotFoundError, IoError, ConfigurationError, EXIT_CODE_SUCCESS

# ---------------------------------------------------------------------------------------------------------------------

# name of the processor
processor_name = 'My Sample Command Processor'

# determines whether the processor is run by the startup script
enabled = True

def get_processor():
    "Returns an instance of the processor provided by the command processor plugin."
    return SampleCommandProcessor()

# ---------------------------------------------------------------------------------------------------------------------


class SampleCommandProcessor(CommandProcessor):

    # -------------------------------------------------------------------------------------------

    def __init__(self):

        # let base class perform its initialization
        super().__init__()

        # register command handlers
        self.add_handler(self.run,             PositionalArgument("run"))
        self.add_handler(self.run,             PositionalArgument("run-and-enter"))
        self.add_handler(self.handle_command1, PositionalArgument("cmd1"))
        self.add_handler(self.handle_command2, PositionalArgument("cmd2"), PositionalArgument("arg1"),
                                               NamedArgument("password", from_stdin=True),
                                               NamedArgument("my-option", min_occurrence=0, max_occurrence=2))

    # -------------------------------------------------------------------------------------------

    def run(self, pos_args, named_args):
        Log.write_note("Configuring service in the container before starting up...")
        return EXIT_CODE_SUCCESS

    # -------------------------------------------------------------------------------------------

    def handle_command1(self, pos_args, named_args):
        print("Handling command 1 (pos_args = {0}, named_args = {1})...".format(pos_args, named_args))
        return EXIT_CODE_SUCCESS

    # -------------------------------------------------------------------------------------------

    def handle_command2(self, pos_args, named_args):
        print("Handling command 2 (pos_args = {0}, named_args = {1})...".format(pos_args, named_args))
        return EXIT_CODE_SUCCESS
        
```

This command processor plugin will handle commands like the following:
```
1)                    docker run     griffinplus/base run
2)                    docker run -it griffinplus/base run-and-enter
3)                    docker run     griffinplus/base cmd1
4)                    docker run     griffinplus/base cmd1 xxx yyy
5)                    docker run     griffinplus/base cmd2 arg1
6)                    docker run     griffinplus/base cmd2 arg1 --password=secret --my-option=abc
7) echo "topsecret" | docker run -i  griffinplus/base cmd2 arg1 --my-option=abc --my-option=xyz
```

Commands 1 and 2 initialize the container invoking the `run()` method and start the service shipped in the container, if the handler returns with exit code 0 (`EXIT_CODE_SUCCESS`). In addition to that, command 2 opens a shell at the end, so the container can be inspected which is quite useful when debugging. The positional arguments (`pos_args`) are `['run']` respectively `['run-and-enter'])` in these cases. Named arguments were not defined at the time the handler was registered, so `named_args` is simply `{}`.

Command 3 and 4 run the `handle_command1()` method with `pos_args` being `['cmd1', 'arg1']` respectively `['cmd1', 'arg1', 'xxx', 'yyy']`. Since the handler was registered without named arguments, `named_args` is simply `{}`.

Command 5, 6 and 7 invoke the `handle_command2()` method with `pos_args` being `['cmd2', 'arg1']` and `named_args` containing entries for the registered named arguments `password` and `my-option`. Command 5 does neither specify any of the registered named arguments in the command line nor does it pipe in anything via *stdin*, so `named_args` is `{ 'password' : [], 'my-option' : [] }`. Command 6 populates the dictionary with command line arguments only, so `named_args` is `{ 'password' : ['secret'], 'my-option' : ['abc'] }`. Command 7 populates `password` via *stdin* and `my-option` from the command line, so `named_args` is `{ 'password' : ['topsecret'], 'my-option' : ['abc', 'xyz'] }`. Piping in confidential information (like credentials) via *stdin* is strictly recommended as confidential information cannot leak via inspection features of the Docker Engine API or process lists that disclose command line parameters.
