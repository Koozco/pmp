import operator
import random as stdrandom
from typing import List, Any, Dict


class RandomUtils:

    def chooseOne(self, list: List[Any]) -> Any:
        idx = stdrandom.randint(0, len(list) - 1)
        return list[idx]

    def keyOfMaxFromDict(self, dictionary: Dict[Any, Any], max_key: Any) -> Any:
        iteritems = dictionary.items()
        stdrandom.shuffle(iteritems)
        return max(iteritems, key=max_key)[0]

    def keyOfMaxValueFromDict(self, dictionary: Dict[Any, Any]) -> Any:
        iteritems = [(k, v) for k, v in dictionary.items()]
        stdrandom.shuffle(iteritems)
        return max(iteritems, key=operator.itemgetter(1))[0]

    def keyOfMinValueFromDict(self, dictionary: Dict[Any, Any]) -> Any:
        iteritems = [(k, v) for k, v in dictionary.items()]
        stdrandom.shuffle(iteritems)
        return min(iteritems, key=operator.itemgetter(1))[0]

    def random(self) -> float:
        return stdrandom.random()

    def randint(self, a: int, b: int) -> int:
        return stdrandom.randint(a, b)

    def shuffle(self, c: List[Any]) -> List[Any]:
        return stdrandom.shuffle(c)

    pass
