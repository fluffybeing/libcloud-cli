import logging

from cliff import lister

from openstackclient.common import exceptions as exc
from openstackclient.common import utils


class ListExtension(lister.Lister):
    """List extension command"""

    log = logging.getLogger(__name__ + '.ListExtension')

    def get_parser(self, prog_name):
        parser = super(ListExtension, self).get_parser(prog_name)
        parser.add_argument(
            '--long',
            action='store_true',
            default=False,
            help='List additional fields in output')
        parser.add_argument(
            '--identity',
            action='store_true',
            default=False,
            help='List extensions for the Identity API')
        return parser

