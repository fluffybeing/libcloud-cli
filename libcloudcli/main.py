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
#from commands import AWS, File, Files, Compute, CreateNode

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

#import libcloudcli
#from libcloudcli.apps import commandmanager
from apps import commandmanager
from common import utils


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

        # Replace the cliff-added help.HelpAction to defer its execution
        self.DeferredHelpAction = None
        for a in self.parser._actions:
            if type(a) == help.HelpAction:
                # Found it, save and replace it
                self.DeferredHelpAction = a

                # These steps are argparse-implementation-dependent
                self.parser._actions.remove(a)
                if self.parser._option_string_actions['-h']:
                    del self.parser._option_string_actions['-h']
                if self.parser._option_string_actions['--help']:
                    del self.parser._option_string_actions['--help']

                # Make a new help option to just set a flag
                self.parser.add_argument(
                    '-h', '--help',
                    action='store_true',
                    dest='deferred_help',
                    default=False,
                    help="Show this help message and exit",
                )
        '''
        commands = {
            'aws': AWS,
            'file': File,
            'files': Files,
            'compute': Compute,
            'createnode': CreateNode
        }
        for k, v in commands.iteritems():
            ex_command.add_command(k, v)
        '''

    def authenticate_user(self):
        """Make sure the user has provided all of the authentication
        info we need.
        """
        self.log.debug('validating authentication options')
        # use also the options parser for it
        # get the provider
        # authenticate with the provider with libcloud api
        Driver = get_driver(Provider.RACKSPACE)
        self.client_manager = Driver(
            'ABCD', 'XYZ',
            datacenter='us-central1-a',
            project='your_project_id'
            )

        return

    def run(self, argv):
        try:
            return super(LibcloudCLI, self).run(argv)
        except Exception as e:
            if not logging.getLogger('').handlers:
                logging.basicConfig()
            if self.dump_stack_trace:
                self.log.error(traceback.format_exc(e))
            else:
                self.log.error('Exception raised: ' + str(e))
            return 1

    def build_option_parser(self, description, version):
        parser = super(LibcloudCLI, self).build_option_parser(
            description,
            version)

        parser.add_argument(
            '--username',
            metavar='<username>',
            default=utils.env('USERNAME'),
            help='Authentication username')
        parser.add_argument(
            '--password',
            metavar='<password>',
            default=utils.env('PASSWORD'),
            help='Authentication password')
        return parser

    def initialize_app(self, argv):
        self.log.debug('initialize_app')
        super(LibcloudCLI, self).initialize_app(argv)

        # Set requests logging to a useful level
        requests_log = logging.getLogger("requests")
        if self.options.debug:
            requests_log.setLevel(logging.DEBUG)
            self.dump_stack_trace = True
        else:
            requests_log.setLevel(logging.WARNING)
            self.dump_stack_trace = False

        # Commands that span multiple APIs
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

        # Handle deferred help and exit
        if self.options.deferred_help:
            self.DeferredHelpAction(self.parser, self.parser, None, None)

    def prepare_to_run_command(self, cmd):
        self.log.debug('prepare_to_run_command %s', cmd.__class__.__name__)

        if not cmd.auth_required:
            return
        if cmd.best_effort:
            try:
                self.authenticate_user()
            except Exception:
                pass
        else:
            self.authenticate_user()
        return

    def clean_up(self, cmd, result, err):
        self.log.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.log.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    app = LibcloudCLI()
    return app.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
