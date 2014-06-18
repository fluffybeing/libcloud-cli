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
def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)

        data = {}
        # Get module versions
        mods = sys.modules
        for k in mods.keys():
            k = k.split('.')[0]
            if (parsed_args.all or 'client' in k):
                try:
                    data[k] = mods[k].__version__
                except AttributeError:
                    # aw, just skip it
                    pass

        return zip(*sorted(six.iteritems(data)))

