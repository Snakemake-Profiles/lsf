from typing import TextIO

import yaml


class Config:
    def __init__(self, data: yaml.YAMLObject):
        self._data = data

    def __contains__(self, item) -> bool:
        return item in self._data

    @staticmethod
    def from_stream(stream: TextIO) -> "Config":
        data = yaml.safe_load(stream)
        return Config(data)
