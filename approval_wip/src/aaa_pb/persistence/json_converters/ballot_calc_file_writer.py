from typing import Dict

from aaa_pb.model.ballot_2d2 import ApprovalBallotCalc
from aaa_pb.utils.class_utils import ClassUtils


class ApprovalBallotCalc_JsonConverter:
    @classmethod
    def persist(self, calc: ApprovalBallotCalc) -> Dict[str, str]:
        params_str = " ".join([str(x) for x in calc._get_params()])
        module_name, class_name = ClassUtils.get_module_and_class_name(clazz=calc.__class__)
        return {
            "module_name": module_name,
            "class_name": class_name,
            "params": params_str
        }

    @classmethod
    def load(self, data: Dict[str, str]) -> ApprovalBallotCalc:
        params = data["params"].split(" ")
        float_params = [float(x) for x in params]
        clazz = ClassUtils.get_class(
            module_name=data["module_name"],
            class_name=data["class_name"]
        )
        return clazz(*float_params)
