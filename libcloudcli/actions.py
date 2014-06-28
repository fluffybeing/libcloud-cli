# Copyright 2013 Rackspace
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import argparse


class HelpAction(argparse.Action):
    """
    Custom HelpAction which recognizes commands in <app> command> <sub command>
    format.
    """
    def __call__(self, parser, namespace, values, option_string=None):
        app = self.default
        parser.print_help(app.stdout)
        app.stdout.write('\nCommands:\n')
        command_manager = app.command_manager

        for command, sub_commands in sorted(command_manager):
            for sub_command, ep in sub_commands.items():

                try:
                    factory = ep.load()
                except Exception as err:
                    app.stdout.write('Could not load %r\n' % ep)
                    continue

                try:
                    cmd = factory(self, None)
                except Exception as err:
                    app.stdout.write('Could not instantiate %r: %s\n' %
                                    (ep, err))
                    continue
                one_liner = cmd.get_description().split('\n')[0]

                if sub_command == 'index':
                    name = command
                else:
                    name = '%s %s' % (command, sub_command)

                app.stdout.write('  %-13s  %s\n' % (name, one_liner))
        sys.exit(0)
