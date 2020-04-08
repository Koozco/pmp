from pathlib import Path
from typing import Tuple, List


class ElectionTestDataReader:
    @classmethod
    def _readElectionInstance(cls, data_file_path: Path) -> Tuple[List[List[int]], int]:
        import os
        cwd = os.getcwd()
        print(cwd)
        with open(str(data_file_path)) as f:
            lines = f.readlines()

        number_of_voters = int(lines[0])
        number_of_candidates = int(lines[1])

        assert len(lines) == (2 + number_of_voters)

        V = []
        for line in lines[2:]:
            vote = [int(x) for x in (line.split(" ")) if len(x) > 0]
            V.append(vote)

        return V, number_of_candidates
