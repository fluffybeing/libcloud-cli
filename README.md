Apache Libcloud CLI
===================

About
-----
Apache [Libcloud][1] is a standard Python library that abstracts away differences among multiple cloud provider APIs.
Currently Libcloud has a big limitation, you can only use it with Python and you have to write code for each
task, So a CLI for Libcloud will bring up lot of new possibilities to its users and will allow users and system
administrators to perform commonly used operations (listing servers, rebooting servers etc.) easily via
command line without writing a single line of code.

Command line client is available on PyPi and can be installed using pip:

```bash
pip install -r requirements.txt
python setup.py install
```

## Settings Credentials

Credentials can be set (in order of precedence) as environment variables in a
configuration file or you can pass them manually to each command.

Default configuration file path is `~/.libcloudcli/config.ini` but you can overrride it by
setting the `LibcloudCLI_` environment variable

Example configuration files can be found in the `examples/` directory.

## Usage

```bash
libcloudcli <api> <resource> <action> [options]
```

For example:

```bash
libcloudcli compute node create  --id="hello"  --size=""
```

### Custom Output Formatter

To specify a custom formatter, use `-f` option. For example:

`libcloudcli compute node destroy -f json` id="hello"

#### Available Formatters

* table
* csv
* json
* yaml
* html

## Development

### Testing and Lint

Running lint

```bash
tox
```

## Links

* [Strategic plan][2]
* [GSoC Proposal][3]

[1]: http://libcloud.apache.org
[2]: https://docs.google.com/document/d/1j58g98HRJQ6dgUjDd6RAS9qA_e4XwFd1x89m2PIPL4M/edit?usp=sharing
[3]: https://docs.google.com/document/d/1dLtEsHsdj_h6dyrugycKDYV26ihfsZMaRJ9rElZ2TtM/edit?usp=sharing
