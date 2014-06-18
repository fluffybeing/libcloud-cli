"""Module action implementation"""

import logging
import six
import sys

from cliff import show


class ListModule(show.ShowOne):
    """List module versions"""

    auth_required = False
    log = logging.getLogger(__name__ + '.ListModule')

    def get_parser(self, prog_name):
        parser = super(ListModule, self).get_parser(prog_name)
        parser.add_argument(
            '--all',
            action='store_true',
            default=False,
            help='Show all modules that have version information',
        )
        return parser
