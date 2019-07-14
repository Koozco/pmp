import inspect
import sys


def introspect_func(module_name, primary_class):
    classes = []
    module = sys.modules[module_name]
    for name in dir(module):
        obj = getattr(module, name)
        if inspect.isclass(obj) and issubclass(obj, primary_class):
            classes.append(name)
    return classes
