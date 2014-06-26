# -*- coding:utf-8 -*-
# taken from libcloud.REST

import inspect
import re

#from libcloud.utils.misc import get_driver
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

from parinx.parser import parse_args, ARGS_TO_XHEADERS_DICT, \
    parse_docstring, get_method_docstring

from libcloudcli.errors import ProviderNotSupportedError,\
    MissingArguments, MissingHeadersError, MethodParsingException,\
    NoSuchOperationError

from parinx.utils import json


class DriverMethod(object):
    _type_name_pattern = r'.\{([_0-9a-zA-Z]+)\}'

    def __init__(self, driver_obj, method_name):
        if inspect.isclass(driver_obj):
            self.driver_cls = driver_obj
        else:
            self.driver_cls = driver_obj.__class__

        self.driver_obj = driver_obj
        self.method_name = method_name
        self.method = getattr(self.driver_obj, method_name, None)

        if not inspect.ismethod(self.method):
            raise NoSuchOperationError()
        method_doc = get_method_docstring(self.driver_cls, method_name)

        if not method_doc:
            raise MethodParsingException('Empty docstring')

        argspec_arg = parse_args(self.method)
        docstring_parse_result = parse_docstring(method_doc, self.driver_cls)
        self.description = docstring_parse_result['description']
        docstring_args = docstring_parse_result['arguments']

        #check vargs
        self.vargs_entries = []
        self.req_vargs_entries = []
        for name, arg_info in docstring_args.items():
            docstring_arg_tmp = docstring_args[name]
            #print docstring_arg_tmp
            entry_kwargs = {
                'name': name,
                'description': docstring_arg_tmp['description'],
                'type_name': docstring_arg_tmp['type_name'],
                'required': (docstring_arg_tmp['required'] or
                                arg_info['required']),
            }

            if not entry_kwargs['required']:
                self.vargs_entries.append(entry_kwargs)
            else:
                self.req_vargs_entries.append(entry_kwargs)

        #update kwargs
        kwargs = set(docstring_args).difference(argspec_arg)
        self.kwargs_entries = []
        for entry in kwargs:
            kwargs_entry = {
                'name':entry,
                'description':docstring_args[entry]['description'],
                'type_name':docstring_args[entry]['type_name'],
                'required':docstring_args[entry]['required']
            }
            self.kwargs_entries.append(kwargs_entry)

        method_return = docstring_parse_result['return']
        self.result_entry = method_return
        # For temporary purpose get method argument directly without validation

    @classmethod
    def _remove_type_name_brackets(cls, type_name):
        return re.sub(cls._type_name_pattern, r'\1', type_name)

    def get_arguments(self):
        fields_args = [field.get_description_dict() for field in self._fields]
        if not self.required:
            for field_arg in fields_args:
                field_arg['required'] = False
        return fields_args

    def get_description(self):
        result_arguments = []

        for entry in self.vargs_entries:
            result_arguments.append(entry['name'])

        for entry in self.kwargs_entries:
            result_arguments.append(entry['name'])

        result_arguments = list(set(result_arguments))

        result = {'name': self.method_name,
                  'description': self.description,
                  'arguments': result_arguments,
                  'return': {
                      'type': self._remove_type_name_brackets(
                          self.result_entry['type_name']),
                      'description': self.result_entry['description']}
                  }
        return result

    def invoke_result_to_json(self, value):
        return self.result_entry.to_json(value)

    def invoke(self, data):
        vargs = [e.from_json(data, self.driver_obj)
                 for e in self.vargs_entries]
        kwargs = {}
        for kw_entry in self.kwargs_entries:
            try:
                kwargs[kw_entry.name] = kw_entry.from_json(data,
                                                           self.driver_obj)
            except MissingArguments:
                if kw_entry.required:
                    raise
        if self.method_name == '__init__':
            return self.driver_cls(*vargs, **kwargs)
        return self.method(*vargs, **kwargs)


def get_providers_info():
    """
    List of all supported providers.

    :param providers: object that contain supported providers.
    :type  providers: :class:`libcloud.compute.types.Provider`

    :return `list of dict objects`
    """
    result = []
    for provider, Driver in get_providers_dict().items():
        result.append({
            'id': provider,
            'friendly_name': getattr(Driver, 'name', ''),
            'website': getattr(Driver, 'website', ''),
        })
    return result


def get_providers_dict():
    result = {}
    for provider_name in Provider.__dict__.keys():
        if provider_name.startswith('_'):
            continue

        provider_name = provider_name.upper()
        try:
            Driver = get_driver_by_provider_name(provider_name)
            result[provider_name] = Driver
        except ProviderNotSupportedError:
            continue
    return result


def get_driver_by_provider_name(provider_name):
    """
    Get a driver by provider name
    If the provider is unknown, will raise an exception.

    :param drivers: Dictionary containing valid providers.

    :param provider: object that contain supported provider
    :type providers: :class:`libcloud.compute.types.Provider`

    :param    provider_name:   String with a provider name (required)
    :type     provider_name:   ``str``

    :return: :class:`NodeDriver`

    """
    provider_name = provider_name.upper()

    if ((provider_name == 'RACKSPACE_NOVA_DFW') or (provider_name == 'RACKSPACE_NOVA_BETA') or (provider_name == 'RACKSPACE_NOVA_ORD') or (provider_name == 'RACKSPACE_NOVA_LON')):
        provider_name = 'RACKSPACE'
    elif ((provider_name == 'RACKSPACE_UK')):
        provider_name = 'RACKSPACE_FIRST_GEN'
    else:
        "Name conflict"

    provider = getattr(Provider, provider_name, None)

    try:
        Driver = get_driver(provider)
    except AttributeError:
        raise ProviderNotSupportedError(provider=provider_name)
    return Driver


def get_driver_instance(Driver, **kwargs):
    try:
        json_data = json.dumps(kwargs)
        driver_method = DriverMethod(Driver, '__init__')
        return driver_method.invoke(json_data)
    except MissingArguments, error:
        str_repr = ', '.join([ARGS_TO_XHEADERS_DICT.get(arg, arg)
                              for arg in error.arguments])
        raise MissingHeadersError(headers=str_repr)

if __name__ == '__main__':
    cls = get_driver(Provider.EC2_US_WEST)
    #print dir(cls)
    b = DriverMethod(cls, 'create_node')
    print b.get_description()
    #get_driver_instance(cls)
    #print get_driver_by_provider_name(Provider,  'EC2_US_EAST')
    #print get_providers_dict()
    #print get_providers_info()
    #print Provider.__dict__
