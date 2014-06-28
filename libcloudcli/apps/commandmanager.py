#

"""Modify Cliff's CommandManager"""

import logging
import pkg_resources

import cliff.commandmanager
from collections import defaultdict
from cliff.commandmanager import EntryPointWrapper
from interface import buildCommandClass

LOG = logging.getLogger(__name__)


class CommandManager(cliff.commandmanager.CommandManager):
    """Alters Cliff's default CommandManager behaviour to load additional
       command groups after initialization.
    """
    def __init__(self, namespace, convert_underscores=True):
        self.group_list = []
        self.commands = defaultdict(dict)
        self.namespace = namespace
        self._load_commands()
        super(CommandManager, self).__init__(namespace, convert_underscores)

    def _load_commands(self, group=None):
        '''
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
        '''
        cls = buildCommandClass()

        # name the class according to the command
        command_class = cls.__dict__
        command_class = command_class['name']

        #LOG.debug('Found command %s %s', command_class)

        # this will give the command construct we need
        # i.e $ libcloud <api> <resource> <action>
        _command_construct = cls.get_command_construct()
        api = _command_construct[0]
        resource = _command_construct[1]
        action = _command_construct[2]

        command_name = '%s.%s.%s.%s' % ('libcloudcli', api, resource, action)

        wrapper = EntryPointWrapper(name=command_name,
                                    command_class=command_class)

        if not api in self.commands:
            self.commands[api] = defaultdict(dict)

        # Add this command to command manager
        self.commands[api][resource][action] = wrapper
        return

    def add_command_group(self, group=None):
        """Adds another group of command entrypoints"""
        if group:
            self._load_commands(group)

    def get_command_groups(self):
        """Returns a list of the loaded command groups"""
        return self.group_list
