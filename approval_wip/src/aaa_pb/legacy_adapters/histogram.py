from typing import List

from pathlib import Path

from aaa_pb.legacy import histogram_draw
from aaa_pb.legacy.old_histogram import OldHistogram
from aaa_pb.model.election_result import ElectionResult


class Histogram:

    def __init__(self, old_histogram: OldHistogram) -> None:
        self.old_histogram = old_histogram

    @staticmethod
    def fromElectionResults(election_results: List[ElectionResult]) -> 'Histogram':
        h = OldHistogram(number_of_experiments=None,
                         input_dir_path=None,
                         rule_name_with_committee_size=None)

        for election_result in election_results:
            h.computeHistogramIncrementallySane(election_result.committee_2d)

        return Histogram(h)

    def writeToTextFile(self, path: Path) -> None:
        self \
            .old_histogram \
            .writeHistFileSaner(output_path=path)

    def writeToImageFile(self,
                         path: Path,
                         TRADITIONAL: bool = True,
                         threshold: float = 0.004,
                         col_r: float = 1.0,
                         col_g: float = 0.8,
                         col_b: float = 0.8) -> None:
        W = self.old_histogram.W
        H = self.old_histogram.H
        HISTOGRAM = self.old_histogram.HISTOGRAM

        histogram_draw.drawHistogramSaner2(
            output_file_path=path,
            W=W,
            H=H,
            HISTOGRAM=HISTOGRAM,
            TRADITIONAL=TRADITIONAL,
            threshold=threshold,
            col_r=col_r,
            col_g=col_g,
            col_b=col_b)
