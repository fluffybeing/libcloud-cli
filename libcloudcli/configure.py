import os
import re
import sys
import logging
import configparser


def main():
    try:
        root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        # currently config.ini is in example folder
        config_path = os.path.join(root, 'examples/config.ini')
        # TODO: There is a better way to log this message than print.
        print "Reading secrets from %r" % secret_path

    parser = configparser.ConfigParser()
        parser.read(config_path)
        get_config = dict(parser.items("default"))
    except Exception as e:
        # TODO: There is a better way to log this message than print.
        print 'Failed to load config.ini.  Reason: %r' % str(e)

if __name__ == '__main__':
    main()
