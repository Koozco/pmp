from typing import List, Tuple

from test.test_base import TestBase
from test.test_commons.election_test_data_reader import ElectionTestDataReader
from test.test_commons.election_test_data_source import ElectionTestDataSource


class ApprovalElectionTestDataSource(ElectionTestDataSource):
    test_input_dir_path = TestBase.TEST_INIT_DIR_PATH / "_phragmen_test_data"
    test_input_file_names = [str(x) for x in range(1, 11)]  # [:1] # TODO take just first file because it's slow

    def getSampleElections(self):
        for sample_name in self.test_input_file_names:
            V, number_of_candidates, k = self.__deserializeSampleData(sample_name)
            data = {
                'V': V,
                'number_of_candidates': number_of_candidates,
                'k': k,
                'sample_name': sample_name
            }
            yield data

    def getSamplePhragmenResult(self, sample_name):
        loads, committee = self.__deserializePhragmenResult(sample_name=sample_name)
        data = {
            'loads': loads,
            'committee': committee,
        }
        return data

    def serializeCommitteeAndLoads(self, voter_loads: List[float], committee: List[int], sample_name: str) -> None:
        committee = sorted(committee, key=lambda x: x)

        c_str = " ".join([str(x) for x in committee])
        v_str = " ".join([str(x) for x in voter_loads])

        with open(str(self.test_input_dir_path / (sample_name + "_results")), 'w') as f:
            print >> f, c_str
            print >> f, v_str

    def __deserializePhragmenResult(self, sample_name: str) -> Tuple[List[float], List[int]]:
        with open(str(self.test_input_dir_path / (sample_name + "_phragmen_results")), 'r') as f:
            lines = f.readlines()

        assert len(lines) == 2

        committee = [int(x) for x in lines[0].split(" ")]
        loads = [float(x) for x in lines[1].split(" ")]

        return loads, committee

    def __deserializeSampleData(self, sample_name: str) -> Tuple[List[List[int]], int, int]:
        election_data_file_path = self.test_input_dir_path / sample_name
        V, number_of_candidates = ElectionTestDataReader._readElectionInstance(
            data_file_path=election_data_file_path
        )

        # TODO hardcoded committee size
        input_data = (V, number_of_candidates, 4)

        return input_data

    pass
