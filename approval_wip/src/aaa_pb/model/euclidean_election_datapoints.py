from pathlib import Path
from typing import List, Tuple


class EuclideanElectionDatapoints:

    def __init__(self, V: List[Tuple[float, float]], C: List[Tuple[float, float]]) -> None:
        self.V = V
        self.C = C

    @classmethod
    def fromFile(cls, datapoints_file_path: Path) -> 'EuclideanElectionDatapoints':
        with open(str(datapoints_file_path), mode='r') as input_file:
            lines = input_file.readlines()
            lines_orig_len = len(lines)
            number_of_voters = int(lines[0])
            lines = lines[1:]
            V_str = lines[:number_of_voters]
            lines = lines[number_of_voters:]
            number_of_candidates = int(lines[0])
            lines = lines[1:]
            C_str = lines

            V = [cls.__toFloatPair(x) for x in V_str]
            C = [cls.__toFloatPair(x) for x in C_str]

            assert lines_orig_len == (2 + number_of_candidates + number_of_voters)

            return EuclideanElectionDatapoints(V=V, C=C)
        pass

    def toFile(self, output_file_path: Path) -> None:
        V = self.V
        C = self.C
        V_str = [self.__FloatPairToStr(x) for x in V]
        C_str = [self.__FloatPairToStr(x) for x in C]
        l = [len(V)] + V_str + [len(C)] + C_str
        output_file_path.write_text(data="\n".join(str(x) for x in l))

    @classmethod
    def __toFloatPair(cls, s: str) -> Tuple[float, float]:
        a, b = s.split(",")
        return float(a), float(b)

    def __FloatPairToStr(cls, pair: Tuple[float, float]) -> str:
        a, b = pair
        return str(a) + "," + str(b)
