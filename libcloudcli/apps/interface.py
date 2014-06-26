# interface to link up the methods info and the dynamic class builder

from provider import  DriverMethod, get_providers_info, get_driver_method



# get list of the supported provider
def  providerList():
    result = get_providers_info()
    print result

# get list of methods supported by provider
def provderSupportedMethod():
    pass

# create the instance
def driver_instance():
    pass

# request dynamic builder to create the command class
def buildCommandClass():
    pass

# get method info
def methodInfo()
    pass


