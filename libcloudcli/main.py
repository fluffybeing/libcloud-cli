import logging
import sys

from cliff.app import App
from commands import AWS, File, Files, Compute, CreateNode
from cliff.commandmanager import CommandManager


class LibcloudCLI(App):
    log = logging.getLogger(__name__)

    def __init__(self):
        command = CommandManager('libcloudcli.app')
        super(LibcloudCLI, self).__init__(
            description='Libcloud CLI App',
            version='0.1',
            command_manager=command,
        )
        commands = {
            'aws': AWS,
            'file': File,
            'files': Files,
            'compute': Compute,
            'createnode': CreateNode
        }
        for k, v in commands.iteritems():
            command.add_command(k, v)

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
