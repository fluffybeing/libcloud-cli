
"""Node action implementations"""

import logging
import six

from cliff import command
from cliff import lister
from cliff import show


class CreateNode(show.ShowOne):
    """Create compute Node command"""

    log = logging.getLogger(__name__ + ".create_node")

    def get_parser(self, prog_name):
        parser = super(CreateNode, self).get_parser(prog_name)
        parser.add_argument(
            "name",
            metavar="<name>",
            help="Name of the Node")
        parser.add_argument(
            "size",
            metavar="<size>",
            help="The size of the resource allocated")
        parser.add_argument(
            "image",
            metavar="<image>",
            help="OS image to boot on")
        parser.add_argument(
            "auth",
            metavar="<auth>",
            help="Initial authentication information")
        parser.add_argument(
            "location",
            metavar="<location>",
            help="which data center to create node")
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)
        compute_client = self.app.client_manager.compute
        args = (
            parsed_args.name,
            parsed_args.size,
            parsed_args.image,
            parsed_args.auth,
            parsed_args.location
        )
        Node = compute_client.Node.create(*args)._info.copy()
        return zip(*sorted(six.iteritems(Node)))


class DeleteNode(command.Command):
    """Delete compute agent command"""

    log = logging.getLogger(__name__ + ".DeleteAgent")

    def get_parser(self, prog_name):
        parser = super(DeleteNode, self).get_parser(prog_name)
        parser.add_argument(
            "id",
            metavar="<id>",
            help="ID of agent to delete")
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)
        compute_client = self.app.client_manager.compute
        compute_client.Node.delete(parsed_args.id)
        return


class SetNode(show.ShowOne):
    """Set compute Node command"""

    log = logging.getLogger(__name__ + ".SetAgent")

    def get_parser(self, prog_name):
        parser = super(SetNode, self).get_parser(prog_name)
        parser.add_argument(
            "id",
            metavar="<id>",
            help="ID of the agent")
        parser.add_argument(
            "version",
            metavar="<version>",
            help="Version of the agent")
        parser.add_argument(
            "url",
            metavar="<url>",
            help="URL")
        parser.add_argument(
            "md5hash",
            metavar="<md5hash>",
            help="MD5 hash")
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)
        compute_client = self.app.client_manager.compute
        args = (
            parsed_args.id,
            parsed_args.version,
            parsed_args.url,
            parsed_args.md5hash
        )
        Node = compute_client.Node.update(*args)._info.copy()
        return zip(*sorted(six.iteritems(Node)))
