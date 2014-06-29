"""This is code which will create dynamic classes"""
#  I am using types for this and lamda function

import logging
import six

from cliff import command
from cliff import lister
from cliff import show

from provider import  DriverMethod, get_providers_info
from commandmapper import get_resource_action

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

class DynamicClass(command.Command):

    def __init__(self, app_args):
        self.arguments = app_args['arguments']
        self.action = app_args['action']
        self.name = app_args['name']
        self.api = app_args['api']
        self.resource = app_args['resource']
        self.action = app_args['action']

    def take_action(self, parsed_args):
        args = ()
        for arg in self.arguments:
                args += getattr(parsed_args.arg.keys())
        #result = self.action(args)
        result = "your node is created"
        return result

    def get_parser(self, prog_name):
        parser = super(DynamicClass, self).get_parser(prog_name)
        for arg in self.arguments:
            parser.add_argument(
                arg.keys(),
                metavar="<"+arg.keys()+">",
                help=arg.values())
        return parser

    def get_api(self):
        return self.api

    def get_resource(self):
        return self.resource

    def get_action(self):
        return self.action

    def get_command_construct(self):
        result = [self.api, self.resource, self.action]
        return result
    '''
    def create_command(self, base=None):
        fields = {}

        fields['take_action'] = self.take_action()
        fields['get_parser'] = self.get_parser()

        model = type(self.name, base, fields)

        return model
    '''

if __name__ == '__main__':
    cls = get_driver(Provider.EC2_US_WEST)
    driver = DriverMethod(cls, 'create_node')
    app_args = driver.get_description()
    app_args['api'] = 'compute'
    resource, action = get_resource_action('create_node')
    app_args['resource'] = resource
    app_args['action'] = action
    D = DynamicClass(app_args)
    print D.get_command_construct()
