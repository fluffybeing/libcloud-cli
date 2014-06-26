""" This is code which will create dynamic classes"""
#  I am using types for this and lamda function
#


def create():
    print "create compute agent command"

def delete():
    print "delete compute agent command"

def List():
    print "list compute agent command"

def Set():
    print "set compute agent command"

def create_command(name, base=None, get_parser=None, action_value=None):
    variables = {
        'os': ("os", {'metavar':"<os>", 'help':"Type of OS"}),
        'architecture': ("architecture", {'metavar':"<architecture>", 'help':"Type of architecture"}),
        'version': ("version", {'metavar':"<version>", 'help':"Version"}),
        'url': ("url", {'metavar':"<url>", 'help':"URL"}),
        'md5hash': ("md5hash", {'metavar':"<md5hash>", 'help':"MD5 hash"}),
        'hypervisor': ("hypervisor", {'metavar':"<hypervisor>", 'help':"Type of hypervisor", 'default':"xen"}),
        '--hypervisor': ("--hypervisor", {'metavar':"<hypervisor>", 'help':"Type of hypervisor"}),
        'id': ("id", {'metavar':"<id>", 'help':"ID of the agent"}),
    }

    actions = {"create": create, "delete": delete, "List": List}
    fields = {}
    get_parser_arguments = {}

    for parser in get_parser:
        get_parser_arguments['parser'] = variables[parser]

    action = actions[action_value]
    print action()
    fields['take_action'] = lambda self: action()

    fields['get_parser'] = lambda self: [variables[keys] for keys in get_parser]

    model = type(name, base, fields)

    return model

if __name__ == '__main__':

    model = create_command('CreateAgent', (object,), ['os', 'architecture'], 'create')
    person_instance = model()
    print person_instance.get_parser()
    print person_instance.take_action()
