""" This is code which will create dynamic classes"""
#  I am using types for this and lamda function
#


#### Sample methods for the take actions
def create():
    print "create compute agent command"

def delete():
    print "delete compute agent command"

def List():
    print "list compute agent command"

def Set():
    print "set compute agent command"


def create_command(name, base=None, parser_value=None, action_value=None):
    '''
    :param    name: Name of the command class.
    :type     name: ``str``

    :param    base: object that contain supported provider
    :type     base: :class:`cliff.command.types`

    :param    parser_value: dict containing the options for the parser (required)
    :type     parser_value:   ``dict``

    :param    action_value: methods which will perfrom the action

    :return: :class:`cliff.command.types`
    '''

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

    variables = {
        'username': ("os", {'metavar':"<username>", 'help':"Type the username"}),
        'password': ("password", {'metavar':"<password>", 'help':"Type of password"}),
        'version': ("version", {'metavar':"<version>", 'help':"Version"}),
        'url': ("url", {'metavar':"<url>", 'help':"URL"}),
        'id': ("id", {'metavar':"<id>", 'help':"ID of the agent"}),
        }

    model = create_command('CreateAgent', (object,), ['os', 'architecture'], 'create')
    person_instance = model()
    print person_instance.get_parser()
    print person_instance.take_action()
