"""This is code which will create dynamic classes"""
#  I am using types for this and lamda function

import logging
import six

from cliff import command
from cliff import lister
from cliff import show

from provider import  DriverMethod, get_providers_info

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

class DynamicClass():

    def __init__(self, **kwargs):
        self.arguments = kwargs['arguments']
        self.action = kwargs['action']
        self.name = kwargs['name']

    def take_action(self, parsed_args):
        args = ()
        for arg in self.arguments:
                args += getattr(parsed_args.arg.keys())
        result = self.action(args)
        return result

    def get_parser(self, prog_name):
        parser = super(self.name, self).get_parser(prog_name)
        for arg in self.arguments:
            parser.add_argument(
                arg.keys(),
                metavar="<"+arg.keys()+">",
                help=arg.values())
        return parser

    def create_command(self, base=None):
        fields = {}

        fields['take_action'] = self.take_action()
        fields['get_parser'] = self.get_parser()

        model = type(self.name, base, fields)

        return model


if __name__ == '__main__':
    cls = get_driver(Provider.EC2_US_WEST)
    driver = DriverMethod(cls, 'create_node')
    method_desc = driver.get_description()
    print method_desc
    D =  DynamicClass(method_desc)
    print D.create_command()
