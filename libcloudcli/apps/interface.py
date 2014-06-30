# interface to link up the methods info and the dynamic class builder

from provider import  DriverMethod, get_providers_info, get_driver_methods
from dynamicclass import DynamicClass
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver


# get list of the supported provider
def  providersList():
    result = get_providers_info()
    print result


# get list of methods supported by provider
def providerSupportedMethod(driver, method):
    result = get_driver_methods(driver)
    if method in result:
      return method
    else:
        print "Method doesn't exit with provider"

def get_provider_instance(name):
    Provider = getattr(Provider, name)
    cls = get_driver(Provider.name)
    return cls


# request dynamic builder to create the command class
def buildCommandClass():
    cls = get_driver(Provider.EC2_US_WEST)
    method_desc = methodInfo(cls, 'create_node')
    cls = DynamicClass(method_desc)
    #result = factory(cls, method_desc['name'])
    return cls


# get method info
def methodInfo(driver, method):
    D = DriverMethod(driver, method)
    result = D.get_description()
    return result


# new  name of the class
def factory(BaseClass, name):
    class NewClass(BaseClass):
        pass
    NewClass.__name__ = "%s" % name
    return NewClass

