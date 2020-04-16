from io import StringIO
from tests.src.lsf_config import Config


class TestBool:
    def test_empty_returns_false(self):
        config = Config({})

        assert not config

    def test_non_empty_returns_true(self):
        config = Config({1: 1})

        assert config


class TestDefaultConstructor:
    def test_no_options_given_returns_empty(self):
        config = Config()

        assert not config


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


class TestConcatenateParams:
    def test_str_returns_str(self):
        params = "-q queue"

        actual = Config.concatenate_params(params)
        expected = params

        assert actual == expected

    def test_empty_list_returns_empty_str(self):
        params = []

        actual = Config.concatenate_params(params)
        expected = ""

        assert actual == expected

    def test_list_returns_str(self):
        params = ["-q queue", "-P project"]

        actual = Config.concatenate_params(params)
        expected = "-q queue -P project"

        assert actual == expected


class TestGet:
    def test_get_empty_returns_default(self):
        stream = StringIO("")
        config = Config.from_stream(stream)
        key = "key"

        actual = config.get(key)

        assert actual is None

    def test_get_key_in_yaml(self):
        stream = StringIO("key: 'foo'")
        key = "key"
        config = Config.from_stream(stream)

        actual = config.get(key)
        expected = "foo"

        assert actual == expected

    def test_get_key_not_in_yaml_returns_default(self):
        stream = StringIO("key: 'foo'")
        key = "bar"
        default = "default"
        config = Config.from_stream(stream)

        actual = config.get(key, default)
        expected = default

        assert actual == expected


class TestDefaultParams:
    def test_no_default_returns_empty(self):
        stream = StringIO("key: 'foo'")
        config = Config.from_stream(stream)

        actual = config.default_params()
        expected = ""

        assert actual == expected

    def test_default_present_returns_params(self):
        stream = StringIO("__default__: '-q foo'")
        config = Config.from_stream(stream)

        actual = config.default_params()
        expected = "-q foo"

        assert actual == expected

    def test_default_present_params_are_list_returns_params(self):
        stream = StringIO("__default__:\n  - '-q foo'\n  - '-P project'")
        config = Config.from_stream(stream)

        actual = config.default_params()
        expected = "-q foo -P project"

        assert actual == expected

    def test_default_present_without_underscores_returns_empty(self):
        stream = StringIO("default:\n  - '-q foo'\n  - '-P project'")
        config = Config.from_stream(stream)

        actual = config.default_params()
        expected = ""

        assert actual == expected


class TestParamsForRule:
    def test_no_default_or_rule_returns_empty(self):
        stream = StringIO("key: 'foo'")
        config = Config.from_stream(stream)
        rulename = "a"

        actual = config.params_for_rule(rulename)
        expected = ""

        assert actual == expected

    def test_default_present_but_not_rule_returns_default_params(self):
        stream = StringIO("__default__: '-q foo'")
        config = Config.from_stream(stream)
        rulename = "a"

        actual = config.params_for_rule(rulename)
        expected = "-q foo"

        assert actual == expected

    def test_rule_and_default_present_returns_default_and_rule_params(self):
        stream = StringIO(
            "__default__: '-q foo'\nrule:\n  - '-P project'\n  - '-q bar'"
        )
        config = Config.from_stream(stream)
        rulename = "rule"

        actual = config.params_for_rule(rulename)
        expected = "-q foo -P project -q bar"

        assert actual == expected

    def test_rule_present_but_not_default_returns_rule_params(self):
        stream = StringIO("rule:\n  - '-P project'\n  - '-q bar'")
        config = Config.from_stream(stream)
        rulename = "rule"

        actual = config.params_for_rule(rulename)
        expected = "-P project -q bar"

        assert actual == expected
