from typing import List

from aaa_pb.utils.random_utils import RandomUtils


class ApprovalBasedRuleBase:
    """
    Base class for all approval-based rules

    Features and purposes:
        * automatically register each subclass as new voting rule
        * define a common API for all approval-based rules
    """

    excluded = False

    randomUtils = RandomUtils()

    @classmethod
    def apply(clazz, V: List[List[int]], number_of_candidates: int, k: int) -> List[int]:
        raise NotImplementedError()

    @classmethod
    def getName(cls) -> str:
        return cls.__name__

    @classmethod
    def getShortName(cls) -> str:
        long_name = cls.__name__
        idx = long_name.rfind(".")
        return long_name[idx + 1:]
