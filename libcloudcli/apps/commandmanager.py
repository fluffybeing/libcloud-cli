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

        command_name = '%s.%s.%s.%s.%s' % (self.namespace,'libcloudcli',_command_construct[0],_command_construct[1],_command_construct[2])

        wrapper = EntryPointWrapper(name=command_name,
                                    command_class=command_class)
        # Add this command to command manager
        self.commands[_command_construct[0]][_command_construct[1]][_command_construct[2]] = wrapper
        return

    def add_command_group(self, group=None):
        """Adds another group of command entrypoints"""
        if group:
            self._load_commands(group)

    def get_command_groups(self):
        """Returns a list of the loaded command groups"""
        return self.group_list

    def add_command(self, name, command_class):
        if name == 'help':
            # Overwrite HelpCommand with one which supports commands in the
            # <command> <sub command> class
            command_class = HelpCommand

        self.commands[name]['index'] = EntryPointWrapper(name, command_class)
