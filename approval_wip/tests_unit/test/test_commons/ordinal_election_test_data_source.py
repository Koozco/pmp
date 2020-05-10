from pathlib import Path
from typing import List, Generator, Any

from test.test_commons.election_test_data_reader import ElectionTestDataReader
from test.test_commons.election_test_data_source import ElectionTestDataSource


class OrdinalElectionTestDataSource(ElectionTestDataSource):

    def __init__(self, data_dir: Path, file_names: List[str], k: int) -> None:
        """
        :param data_dir: Points to a directory where the files with individual election are
        """
        self.base_data_dir = data_dir
        self.file_names = file_names
        self.k = k
        pass

    def getSampleElections(self) -> Generator[Any, Any, Any]:
        for file_name in self.file_names:
            election_data_file = self.base_data_dir / file_name
            V = self.__deserializeElection(election_data_file)
            data = {
                'k': self.k,
                'V': V,
                'number_of_candidates': len(V[0]),
                'sample_name': file_name
            }
            yield data

    def __deserializeElection(self, election_data_file: Path) -> List[List[int]]:
        V, _number_of_candidates = ElectionTestDataReader._readElectionInstance(
            data_file_path=election_data_file
        )
        return V

    pass
