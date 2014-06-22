import logging

from cliff import lister

class ListExtension(lister.Lister):

    def get_parser(self, prog_name):
        parser = super(ListExtension, self).get_parser(prog_name)
        parser.add_argument(
            '--long',
            action='store_true',
            default=False,
            help='List additional fields in output')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)' % parsed_args)

        if parsed_args.long:
            columns = ('Name', 'API', 'RESOURCE', 'ACTION')

        data = []
        show_all = (not parsed_args.identity)

        return (columns,
                ((
                    s, columns,
                    formatters={},
                ) for s in data))
