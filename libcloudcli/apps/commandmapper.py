# craete the resource, action to the methods name mapper


RESOURCE = ['node', 'image', 'size', 'volume', 'snapshot', 'key pair', ' public key from file', 'public key from string',
            'balancer', 'member', 'compute node']

ACTION = ['create', 'reboot', 'destroy', 'deploy', 'sizes', 'detach', 'get', 'import', 'list']


def mapper(resource, action):
    ''' return the method after mapping
      we need to validate whether that methods exists or not
      if exists return the mapped method
    '''
    # generally names are joined with '_'
    if (resource in RESOURCE) and (action in ACTION):
        print "hello"
        if resource.split(' '):
            new_name = resource.replace(' ', '_')
        method_name = action + '_' + new_name
    return method_name

if __name__ == '__main__':
    print mapper('node', 'create')


