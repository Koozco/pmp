from typing import Type, Any, Tuple
import sys


class ClassUtils:

    @classmethod
    def get_module_and_class_name(cls, clazz: Type[Any]) -> Tuple[str, str]:
        return (clazz.__module__, clazz.__name__)

    @classmethod
    def get_class(cls, module_name: str, class_name: str) -> Type[Any]:
        return getattr(sys.modules[module_name], class_name)
