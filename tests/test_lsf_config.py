from io import StringIO
from tests.src.lsf_config import Config


class TestContains:
    def test_item_not_in_config(self):
        stream = StringIO("key: 'foo'")
        item = "bar"
        config = Config.from_stream(stream)

        assert item not in config

    def test_item_in_config(self):
        stream = StringIO("key: 'foo'")
        item = "key"
        config = Config.from_stream(stream)

        assert item in config

    def test_only_keys_are_tested_for_membership(self):
        stream = StringIO("key: 'foo'")
        item = "foo"
        config = Config.from_stream(stream)

        assert item not in config
