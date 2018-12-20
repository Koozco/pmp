class MethodRegistry:
    def __init__(self):
        self.all = {}
        self.comments = {}
        self.default = None


def default_methods_registry():
    registry = MethodRegistry()
    registry.all = {'find_committee': 'find_committee'}
    registry.comments = {'find_committee': 'this rule has only one, default algorithm'}
    registry.default = 'find_committee'
    return registry


def solve_methods_registry():
    registry = MethodRegistry()

    def method(name, comment=None, default=False):
        def wrapper(func):
            if default:
                registry.default = name

            if comment is not None:
                registry.comments[name] = comment

            registry.all[name] = func
            return func

        return wrapper

    method.registry = registry
    return method
