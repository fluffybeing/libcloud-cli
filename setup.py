#!/usr/bin/env python

PROJECT = 'libcloudCLI'

# Change docs/sphinx/conf.py too!
VERSION = '0.1'

from setuptools import setup, find_packages

try:
    long_description = open('README.md', 'rt').read()
except IOError:
    long_description = ''

setup(
    name=PROJECT,
    version=VERSION,

    description='Licloud CLI App',
    long_description=long_description,

    author='Tomaz Muraus, Rahul Ranjan',
    author_email='rahul.rrixe@gmail.com',

    url='https://github.com/rahulrrixe/libcloudCLI',
    download_url='https://github.com/rahulrrixe/libcloudCLI/tarball/master',

    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.2',
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                 ],

    platforms=['Any'],

    scripts=[],

    provides=[],
    install_requires=['cliff', 'libcloud_rest', 'configparser'],

    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'libcloudcli = libcloudcli.main:main'
        ],
        'libcloud.cli.compute': [
            'compute_agent_create = libcloudcli.compute.node:CreateAgent',
            'compute_agent_delete = libcloudcli.compute.node:DeleteAgent',
            'compute_agent_set = libcloudcli.compute.node:SetAgent'
        ],
    },

    zip_safe=False,
)
