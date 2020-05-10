from typing import Dict, Any, List, Tuple

from aaa_pb.model.election_instance import ElectionInstance


class ElectionInstance_JsonConverter:

    @classmethod
    def to_json_dict(cls, election: ElectionInstance) -> Dict[str, Any]:
        V = election.V
        C = election.C
        P = election.P

        list_of_voters_2d_points = cls._convert_list_of_points_to_json_repr(data=V)
        list_of_candidates_2d_points = cls._convert_list_of_points_to_json_repr(data=C)
        list_of_preferences = cls._convert_preferences_to_json_repr(P=P, V=V)

        data = {
            "m": len(C),
            "n": len(V),
            "V": list_of_voters_2d_points,
            "C": list_of_candidates_2d_points,
            "P": list_of_preferences,
        }

        # TODO impartial culture won't have 2d coordinates!
        return data

    @classmethod
    def from_json_dict(self, data: Dict[str, Any]) -> ElectionInstance:
        V = self._convert_json_repr_to_list_of_points(data=data["V"])
        C = self._convert_json_repr_to_list_of_points(data=data["C"])
        P = self._convert_json_repr_to_preferences(data=data["P"])

        # TODO these are just stubs for 2d points
        # TODO they should not be part of election instance
        # TODO decouple it
        # C = [0.0] * m
        # V = [0.0] * n

        return ElectionInstance(
            V=V,
            C=C,
            P=P
        )

    @classmethod
    def _convert_preferences_to_json_repr(cls, P: List[List[int]], V: List[Tuple[float, float]]) -> List[str]:
        preference_profiles = []
        for i in range(len(V)):
            x = V[i][0]
            y = V[i][1]
            preference = [x, y] + P[i]
            preference_str = " ".join(str(x) for x in preference)
            preference_profiles.append(preference_str)
        return preference_profiles

    @classmethod
    def _convert_json_repr_to_preferences(cls, data: List[str]) -> List[List[int]]:
        preference_profiles = []
        for voters_preferences in data:
            _x, _y, *P = voters_preferences.split(" ")
            P = [int(x) for x in P]
            preference_profiles.append(P)
        return preference_profiles

    @classmethod
    def _convert_list_of_points_to_json_repr(cls, data: List[Tuple[float, float]]) -> List[str]:
        return [
            f"{point[0]} {point[1]}"
            for point
            in data
        ]

    @classmethod
    def _convert_json_repr_to_list_of_points(cls, data: List[str]) -> List[Tuple[float, float]]:
        result = []
        for point_str in data:
            x, y = point_str.split(" ")
            x = float(x)
            y = float(y)
            result.append((x, y))
        return result
