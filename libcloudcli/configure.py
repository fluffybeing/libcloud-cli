#
#
__all__ = [
    'DEFAULT_ENV_PREFIX',
    'DEFAULT_CONFIG_PATH',

    'get_config'
]

import re
import sys
import logging
import os
from os.path import join as pjoin, expanduser


try:
    import configparser
except ImportError:
    import ConfigParser as configparser

DEFAULT_CREDENTIALS_FILE = '.libcloudcli'
DEFAULT_ENV_PREFIX = 'LIBCLOUDCLI'
DEFAULT_CONFIG_PATH = pjoin(expanduser('~'), DEFAULT_CREDENTIALS_FILE)


def to_bolean(value, default_value=False):
    """
    Convert string value to a boolean.
    """
    if value is None:
        return default_value

    if isinstance(value, bool):
        return value

    return not (value.lower() == 'false')


def get_config(app, default_values=None, config_path=DEFAULT_CONFIG_PATH,
               env_prefix=DEFAULT_ENV_PREFIX, env_dict=None):

    result = {}

    if env_dict is None:
        env_dict = os.environ

    if default_values is None:
        default_values = {}

    keys = [
        ['default', 'username', 'username'],
        ['default', 'api_key', 'api_key'],
        ['default', 'verify_ssl', 'verify_ssl'],
        ['default', 'auth_url', 'auth_url'],
        ['default', 'region', 'region']
    ]

    env_keys = ['username', 'api_key', 'api_url', 'auth-url', 'verify_ssl', 'region']

    for key in env_keys:
        env_key = env_prefix + key
        env_key = env_key.upper()

        if env_key in env_dict:
            result[key] = env_dict[env_key]

    try:
        root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        # currently config.ini is in example folder
        config_path = os.path.join(root, 'examples/config.ini')
        #config_path = env_dict.get(env_prefix + 'LIBCLI', config_path)
        # TODO: There is a better way to log this message than print.
        print "Reading config info from %r" % config_path

        parser = configparser.ConfigParser()
        parser.read(config_path)
        #config_data = dict(parser.items("default"))

        for (config_section, config_key, key) in keys:
            if key in result:
                # Already specified as an env variable
                continue

            # global section
            try:
                value = parser.get(config_section, config_key)
            except configparser.Error:
                pass
            else:
                result[key] = value

            # app specific section
            try:
                value = parser.get(app, config_key)
            except configparser.Error:
                pass
            else:
                result[key] = value

        if 'verify_ssl' in result:
            result['verify_ssl'] = to_bolean(result['verify_ssl'],
                                             default_value=True)

        for key, value in default_values.items():
            if key not in result:
                result[key] = value

        return result

    except Exception as e:
        # TODO: There is a better way to log this message than print.
        print 'Failed to load config.ini.  Reason: %r' % str(e)
