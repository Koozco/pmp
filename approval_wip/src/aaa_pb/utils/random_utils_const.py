from typing import List, Any

from aaa_pb.utils.random_utils import RandomUtils


class RandomUtils_Const(RandomUtils):

    def chooseOne(self, l: List[Any]) -> Any:
        return l[0]
