
# -*- coding:utf-8 -*-
from functools import partial
import re

from libcloud.compute import base as compute_base
from libcloud.compute.drivers import openstack as compute_openstack
from libcloud.compute.drivers import cloudstack as compute_cloudstack
from libcloud.compute.drivers import digitalocean
from libcloud.compute.drivers import ec2
from libcloud.common import gandi as gandi_common
from libcloud.compute.drivers import opennebula as opennebula_compute
from libcloud.common import gogrid as gogrid_common
from libcloud.compute.drivers import gogrid as gogrid_compute
from libcloud.compute.drivers import opsource as opsourse_compute
from libcloud.compute.drivers import vcloud as vcloud_compute
from libcloud.compute.drivers import ibm_sce as ibm_sce_compute
from libcloud.dns import types as dns_types
from libcloud.dns import base as dns_base
from libcloud.loadbalancer import base as lb_base
from libcloud.loadbalancer.drivers import rackspace as lb_rackspace
from libcloud.storage import base as storage_base

from libcloud_rest.utils import json, DateTimeJsonEncoder
from libcloud_rest.api import validators as valid
from libcloud_rest.errors import MalformedJSONError, ValidationError,\
    MissingArguments, TooManyArgumentsError


class Field(object):
    """
    Base class for all field types.
    """
    validator_cls = None
    type_name = None

    def __init__(self, description=None, name=None, required=True):
        self.description = description
        self.name = name
        self._required = required
        self.validator = self.validator_cls(required=required, name=name)

    def _set_required(self, required):
        self._required = required

    def _get_required(self):
        return self._required

    required = property(_get_required, _set_required)

    def validate(self, json_data):
        try:
            data = json_data[self.name]
        except (KeyError, TypeError):
            if self.required:
                raise MissingArguments([self.name])
            return
        self.validator(data)

    def contribute_to_class(self, cls, name):
        self.model = cls
        self.name = name
        self.validator.name = name

    def get_description_dict(self):
        return {'name': self.name,
                'description': self.description,
                'type': self.type_name,
                'required': self.required}

class Entry(object):
    _container_regex = re.compile('(.\{[_0-9a-zA-Z]+\} of .\{[_0-9a-zA-Z]+\})')

    def __new__(cls, name, type_name, description='', required=True, **kwargs):
        if not ' or ' in type_name:
            if type_name in simple_types_fields:
                entry_class = SimpleEntry
            elif LibcloudObjectEntryBase.get_entry(type_name):
                entry_class = LibcloudObjectEntryBase.get_entry(type_name)
            elif re.match(cls._container_regex, type_name):
                entry_class = ListEntry
            else:
                raise ValueError('Unknown type name %s' % (type_name))
            return entry_class(
                name, type_name, description, required, **kwargs)
        return OneOfEntry(name, type_name, description, required, **kwargs)
