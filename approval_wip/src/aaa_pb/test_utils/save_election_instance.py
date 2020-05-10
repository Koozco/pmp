from pathlib import Path
from typing import List

from aaa_pb.utils.json_utils import JsonUtils


class SaveElectionInstance:
    base_output_dir: Path = None

    def __init__(self) -> None:
        self._file_number = 0

    def apply(self, V: List[list], k: int, number_of_candidates: int) -> None:
        if self.base_output_dir is not None:
            self._persist_election_instance(
                V=V,
                k=k,
                number_of_candidates=number_of_candidates,
                base_output_dir=self.base_output_dir
            )

    def _persist_election_instance(self, V: List[list], k: int, number_of_candidates: int,
                                   base_output_dir: Path) -> None:
        self._file_number += 1

        if not base_output_dir.exists():
            base_output_dir.mkdir()

        output_file = self.base_output_dir / str(self._file_number)
        # TODO Persist as JSON
        data = {
            "number_of_voters": len(V),
            "number_of_candidates": number_of_candidates,
            "votes": V
        }
        JsonUtils.write_json_file(path=output_file, data=data)
