import logging
import os

from cliff.command import Command
from cliff.show import ShowOne
from cliff.lister import Lister
from interface import  providerList


class Discover(Command):
    "A simple command that prints a message."

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Discover, self).get_parser(prog_name)
        parser.add_argument(
            "providers",
            metavar="<providers>",
            help="returns lists of supported provider")
        parser.add_argument(
            "provider",
            metavar="<provider>",
            help="returns the provider info")
        parser.add_argument(
            "methods",
            metavar="<methods>",
            help="retuns supported methods")

        return parser

    def take_action(self, parsed_args):
        if parsed_args.providers:
            return providerList()
        else:
            print "adding more subcommands"

