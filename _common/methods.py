class MethodRegistry:
    def __init__(self):
        self.all = {}
        self.comments = {}
        self.default = None


def solve_methods_registry():
    registry = MethodRegistry()

    def method(name, comment=None, default=False):
        def wrapper(func):
            if default:
                registry.default = func

            if comment is not None:
                registry.comments[name] = comment

            registry.all[name] = func
            return func

        return wrapper

    method.registry = registry
    return method
