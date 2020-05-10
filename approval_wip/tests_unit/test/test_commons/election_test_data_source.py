from typing import List, Dict, Any


class ElectionTestDataSource(object):

    def getSampleElections(self) -> List[Dict[Any, Any]]:
        raise NotImplementedError()
