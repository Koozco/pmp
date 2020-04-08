import json
from pathlib import Path
from typing import Dict, Any


class JsonUtils:

    @classmethod
    def write_json_file(cls, path: Path, data: Dict[str, Any]) -> None:
        with open(str(path), "w") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def read_json_file(cls, path: Path) -> Dict[str, Any]:
        with open(str(path)) as f:
            return json.load(f)

    @classmethod
    def to_pretty_json(cls, data: Dict[str, Any]) -> str:
        return json.dumps(data, indent=2, sort_keys=True)

    # @classmethod
    # def dict_to_string(cls, d: Dict[str, Any]) -> str:
    #     pass
