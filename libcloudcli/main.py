import argparse
import getpass
import logging
import os
import sys
import traceback

from cliff.app import App
from cliff import command
from cliff import complete
from cliff import help
from commands import AWS, File, Files, Compute, CreateNode

import libcloudcli
from libcloudcli.apps import commandmanager


class LibcloudCLI(App):

    CONSOLE_MESSAGE_FORMAT = '%(levelname)s: %(name)s %(message)s'

    log = logging.getLogger(__name__)

    def __init__(self):
        # Patch command.Command to add a default auth_required = True
        command.Command.auth_required = True
        command.Command.best_effort = False
        # but for help there should not be any authorisation
        help.HelpCommand.auth_required = False
        complete.CompleteCommand.best_effort = True

        ex_command = commandmanager.CommandManager('libcloud.cli')
        super(LibcloudCLI, self).__init__(
            description='Libcloud CLI App',
            version='0.1',
            command_manager=ex_command,)

        # Show stack traces
        self.dump_stack_trace = True

        # This is instantiated in initialize_app() only when using
        # password flow auth
        self.auth_client = None

        # Assume TLS host certificate verification is enabled
        self.verify = True

        commands = {
            'aws': AWS,
            'file': File,
            'files': Files,
            'compute': Compute,
            'createnode': CreateNode
        }
        for k, v in commands.iteritems():
            ex_command.add_command(k, v)

    def initialize_app(self, argv):
        self.log.debug('initialize_app')

    def prepare_to_run_command(self, cmd):
        self.log.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.log.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.log.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    app = LibcloudCLI()
    return app.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
