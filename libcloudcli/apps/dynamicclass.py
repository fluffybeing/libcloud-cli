
#name - The name of the command which we want to create (``str``) samajh me aaya
#module - the module or methods you want to create in the class (``dict``)
#options - The options which we want to have for the command (``dict``)

def create_command_class(command_name, app_label='', module=None, options=None):
    """
    Create specified command
    """
    class Meta:
        # Using type('Meta', ...) gives a dictproxy error during command creation
        pass

    if app_label:
        # app_label must be set using the Meta inner class
        setattr(Meta, 'app_label', app_label)

    # Update Meta with any options that were provided
    if options is not None:
        for key, value in options.iteritems():
            setattr(Meta, key, value)

    # Add in any fields that were provided
    if fields:
        attrs.update(fields)

    # Create the class, which automatically triggers ModelBase processing
    command_name = type(command_name, (), attrs)


    return command_name

if __name__ == '__main__':
    fields = {
        'first_name': object.int,
        'last_name': object.int,·
        '__str__': lambda self: '%s %s' (self.first_name, self.last_name),}
    model = create_model('Person', fields)
    print len(model._meta.fields)
~