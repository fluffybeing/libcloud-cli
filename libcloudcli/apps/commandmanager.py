#

"""Modify Cliff's CommandManager"""

import logging
import pkg_resources

import cliff.commandmanager


LOG = logging.getLogger(__name__)


class CommandManager(cliff.commandmanager.CommandManager):
    """Alters Cliff's default CommandManager behaviour to load additional
       command groups after initialization.
    """
    def __init__(self, namespace, convert_underscores=True):
        self.group_list = []
        super(CommandManager, self).__init__(namespace, convert_underscores)

    def _load_commands(self, group=None):
        if not group:
            group = self.namespace
        self.group_list.append(group)
        for ep in pkg_resources.iter_entry_points(group):
            LOG.debug('found command %r' % ep.name)
            cmd_name = (
                ep.name.replace('_', ' ')
                if self.convert_underscores
                else ep.name
            )
            self.commands[cmd_name] = ep
        return

    def add_command_group(self, group=None):
        """Adds another group of command entrypoints"""
        if group:
            self._load_commands(group)

    def get_command_groups(self):
        """Returns a list of the loaded command groups"""
        return self.group_list
