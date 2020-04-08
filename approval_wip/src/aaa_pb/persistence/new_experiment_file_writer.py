from pathlib import Path

from aaa_pb.legacy import visualize
from aaa_pb.model.election_result import ElectionResult


class NewExperimentFileWriter:

    @staticmethod
    def writeToTextFile(election_result: ElectionResult, path: Path) -> None:
        W = election_result.committee
        C = election_result.candidates_2d
        V = election_result.voters_2d
        k = election_result.committee_size
        m = election_result.number_of_candidates
        n = election_result.number_of_voters
        P = election_result.voter_preferences

        lines = [
            f"{m} {n} {k}"
        ]

        for p in C:
            x = p[0]
            y = p[1]
            lines.append(
                f"{x} {y}"
            )

        for i in range(n):
            x = V[i][0]
            y = V[i][1]
            preferences_string = " ".join([str(p) for p in (P[i])])
            lines.append(
                f"{x} {y} {preferences_string}"
            )

        for i in sorted(W):
            candidate = C[i]
            lines.append(
                f"{candidate[0]} {candidate[1]}"
            )

        path.write_text(
            data="\n".join(lines)
        )

    @staticmethod
    def writeToImageFile(election_result: ElectionResult, path: Path) -> None:

        winner_points = election_result.committee_2d
        C = election_result.candidates_2d
        V = election_result.voters_2d
        k = election_result.committee_size
        rule_name = election_result.rule_class.getName()

        visualize.drawVisualizationSane(
            C=C,
            V=V,
            Winner=winner_points,
            img_file_output_path=path,
            rule_name=rule_name + "_" + str(k))

        pass
