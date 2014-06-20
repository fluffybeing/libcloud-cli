### this is an example module for
### to achieve the  <api> <resource> <construct>
### using argparse subcommand feature



import logging
import os

from cliff.command import Command
from cliff.show import ShowOne
from cliff.lister import Lister


class AWS(Command):
    "A simple command that prints a message."

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(AWS, self).get_parser(prog_name)
        subparser1 = parser.add_subparsers(help='sub-command help')

        # add a subcommand
        parser_a = subparser1.add_parser('dns', help='dns help')
        #parser_a.add_argument('value', type=str, help='value help')

        # add a subcommand of a subcommand
        subparser2 = parser_a.add_subparsers(help='child sub-command help')
        parser_b = subparser2.add_parser('ipv4', help='ipv4 help')
        parser_b.add_argument('ipval', type=str, help='value help')

        return parser

    def take_action(self, parsed_args):
        self.log.info('sending greeting')
        self.log.debug('debugging')
        self.app.stdout.write('AWS FILED \n')


class File(ShowOne):
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(File, self).get_parser(prog_name)
        parser.add_argument('filename', nargs='?', default='.')

        return parser

    def take_action(self, parsed_args):
        stat_data = os.stat(parsed_args.filename)
        columns = ('Name',
                   'Size',
                   'UID',
                   'GID',
                   'Modified Time',
                   )
        data = (parsed_args.filename,
                stat_data.st_size,
                stat_data.st_uid,
                stat_data.st_gid,
                stat_data.st_mtime,
                )
        return (columns, data)


class Files(Lister):
    """Show a list of files in the current directory.

    The file name and size are printed by default.
    """

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        return (('Name', 'Size'),
               ((n, os.stat(n).st_size) for n in os.listdir('.')))


class Compute(Command):
    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        #self.log.info('sending greeting')
        self.log.debug('debugging')
        self.app.stdout.write('Compute Filed\n')


class CreateNode(Command):
    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        #self.log.info('Sending greeting')
        self.log.info('debugging')
        self.log.info('Creating Node\n')
