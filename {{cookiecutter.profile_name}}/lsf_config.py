from typing import TextIO, Union, List, Any

import yaml


class Config:
    def __init__(self, data: dict = None):
        if data is None:
            data = dict()
        self._data = data

    def __bool__(self) -> bool:
        return bool(self._data)

    def __contains__(self, item) -> bool:
        return item in self._data

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    @staticmethod
    def concatenate_params(params: Union[List[str], str]) -> str:
        if isinstance(params, str):
            return params
        return " ".join(params)

    def default_params(self) -> str:
        return self.concatenate_params(self.get("__default__", ""))

    def params_for_rule(self, rulename: str) -> str:
        default_params = self.default_params()
        rule_params = self.concatenate_params(self.get(rulename, ""))
        return " ".join(params for params in [default_params, rule_params] if params)

    @staticmethod
    def from_stream(stream: TextIO) -> "Config":
        data = yaml.safe_load(stream)
        return Config(data) if data is not None else dict()
