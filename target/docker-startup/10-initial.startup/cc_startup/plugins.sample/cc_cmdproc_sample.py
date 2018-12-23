"""
This module contains a sample implementation of a command processing plugin.
Author: Sascha Falk <sascha@falk-online.eu>
License: MIT License
"""

import os

from ..cc_log import Log
from ..cc_cmdproc import CommandProcessor, PositionalArgument, NamedArgument
from ..cc_errors import GeneralError, CommandLineArgumentError, FileNotFoundError, IoError, ConfigurationError, EXIT_CODE_SUCCESS

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

        Log.write_note("Configuring services in the container before supervisord starts up...")
        return EXIT_CODE_SUCCESS

    # -------------------------------------------------------------------------------------------

    def handle_command1(self, pos_args, named_args):
        print("Handling command 1 (pos_args = {0}, named_args = {1})...".format(pos_args, named_args))
        return EXIT_CODE_SUCCESS

    # -------------------------------------------------------------------------------------------

    def handle_command2(self, pos_args, named_args):
        print("Handling command 2 (pos_args = {0}, named_args = {1})...".format(pos_args, named_args))
        return EXIT_CODE_SUCCESS
