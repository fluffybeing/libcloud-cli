import argparse
import getpass
import logging
import os
import sys
import traceback

from actions import HelpAction
from cliff.app import App
from cliff import command
from cliff import complete
from cliff import help

import libcloud
from apps import commandmanager, discover


class Libcloudcli(App):

    CONSOLE_MESSAGE_FORMAT = '%(levelname)s: %(name)s %(message)s'

    log = logging.getLogger(__name__)

    def __init__(self):
        # Patch command.Command to add a default auth_required = True
        command.Command.auth_required = False
        command.Command.best_effort = False
        # but for help there should not be any authorisation
        help.HelpCommand.auth_required = False
        complete.CompleteCommand.best_effort = True

        lib_command = commandmanager.CommandManager('libcloudcli')
        super(Libcloudcli, self).__init__(
            description='Libcloud Command Line Interface Client',
            version='0.1',
            command_manager=lib_command)
        # Show stack traces
        self.dump_stack_trace = True

        # This is instantiated in initialize_app() only when using
        # password flow auth
        self.auth_client = None

        # Assume TLS host certificate verification is enabled
        self.verify = False

        # To do Replace the cliff-added help.HelpAction to defer its execution

        commands = {
            'discover': discover.Discover,
        }

        for k, v in commands.iteritems():
            #command.add_command(k, v)
            lib_command.add_command(k, v)

    def run(self, argv):
        try:
            return super(Libcloudcli, self).run(argv)
        except Exception as e:
            if not logging.getLogger('').handlers:
                logging.basicConfig()
            if self.dump_stack_trace:
                self.log.error(traceback.format_exc(e))
            else:
                self.log.error('Exception raised: ' + str(e))
            return 1

    def build_option_parser(self, description, version):
        argparse_kwargs = {'conflict_handler': 'resolve'}
        parser = super(Libcloudcli, self).build_option_parser(
            description,
            version,
            argparse_kwargs=argparse_kwargs)

        parser.add_argument(
            '-h', '--help',
            action=HelpAction,
            nargs=0,
            default=self,
            help='show this help message and exit'
        )
        return parser

    def initialize_app(self, argv):
        self.log.debug('initialize_app')
        super(Libcloudcli, self).initialize_app(argv)

        # Commands that span multiple APIs
        # this was to group command commands in one
        self.command_manager.add_command_group(
            'libcloud.common')

        self.command_manager.add_command_group(
            'libcloud.compute')

        self.command_manager.add_command_group(
            'libcloud.dns')

        self.command_manager.add_command_group(
            'libcloud.storage')

        self.command_manager.add_command_group(
            'libcloud.loadbalancer')

    def prepare_to_run_command(self, cmd):
        self.log.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.log.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.log.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    if '--debug' in argv:
        # TODO: improve --debug support, done here very early so we can
        # see everything possible.
        file_path = '/dev/stderr'
        file_handle = open(file_path, 'a')
        libcloud.enable_debug(file_handle)
        logging.basicConfig(filename=file_path,
                            filemode='w',
                            level=logging.DEBUG)
    app = Libcloudcli()
    return app.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
