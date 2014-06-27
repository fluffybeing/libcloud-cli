# interface to link up the methods info and the dynamic class builder

from provider import  DriverMethod, get_providers_info, get_driver_method
from dynamicclass import DynamicClass


# get list of the supported provider
def  providerList():
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
    method_desc = methodInfo(driver, method)
    D = DynamicClass(method_desc)

    return D


# get method info
def methodInfo(driver, method):
    D = DriverMethod(cls, Method)
    result = D.get_description()
    return result


