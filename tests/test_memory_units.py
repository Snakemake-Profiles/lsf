import pytest

from tests.src.memory_units import (
    Unit,
    InvalidSuffix,
    InvalidPower,
    Memory,
    InvalidMemoryString,
)


class TestUnitFromSuffix:
    def test_from_b_returns_bytes(self):
        suffix = "B"

        actual = Unit.from_suffix(suffix)
        expected = Unit.BYTES

        assert actual == expected

    def test_from_gb_returns_giga(self):
        suffix = "GB"

        actual = Unit.from_suffix(suffix)
        expected = Unit.GIGA

        assert actual == expected

    def test_from_lowercase_mb_returns_mega(self):
        suffix = "mb"

        actual = Unit.from_suffix(suffix)
        expected = Unit.MEGA

        assert actual == expected

    def test_invalid_suffix_raises_error(self):
        suffix = "OB"

        with pytest.raises(InvalidSuffix) as error:
            Unit.from_suffix(suffix)

        assert error.match("Valid suffixes are")


class TestUnitFromPower:
    def test_from_1_returns_kilo(self):
        power = 1

        actual = Unit.from_power(power)
        expected = Unit.KILO

        assert actual == expected

    def test_from_invalid_power_raises_error(self):
        power = 10

        with pytest.raises(InvalidPower) as error:
            Unit.from_power(power)

        assert error.match("Valid powers are")


# some trivial getter tests
def test_memory_power():
    mem = Memory(3, Unit.MEGA)

    actual = mem.power
    expected = 2

    assert actual == expected


def test_memory_suffix():
    mem = Memory(3, Unit.EXA)

    actual = mem.suffix
    expected = "EB"

    assert actual == expected


class TestMemoryBytes:
    def test_memory_is_bytes_no_conversion_needed(self):
        value = 40
        mem = Memory(value)

        actual = mem.bytes()
        expected = value

        assert actual == expected

    def test_memory_is_megabytes_conversion_needed(self):
        value = 40
        unit = Unit.MEGA
        mem = Memory(value, unit)

        actual = mem.bytes()
        expected = 40000000

        assert actual == expected

    def test_memory_is_kilobytes_nondecimal_returns_power_of_two(self):
        value = 40
        unit = Unit.KILO
        mem = Memory(value, unit)

        actual = mem.bytes(decimal_multiples=False)
        expected = 40960

        assert actual == expected

    def test_memory_is_bytes_nondecimal_no_conversion_needed(self):
        value = 50
        mem = Memory(value)

        actual = mem.bytes()
        expected = value

        assert actual == expected

    def test_float_as_value(self):
        value = 0.5
        unit = Unit.GIGA
        mem = Memory(value, unit)

        actual = mem.bytes()
        expected = 500000000

        assert actual == expected

    def test_large_floats_comparison(self):
        value = 500
        unit = Unit.ZETTA
        mem = Memory(value, unit)

        actual = mem.bytes()
        expected = float(500000000000000000000000)

        assert actual == expected


class TestRepr:
    def test_round_number_returns_int(self):
        memory = Memory(50, Unit.KILO)

        actual = str(memory)
        expected = "50KB"

        assert actual == expected

    def test_round_float_number_returns_int(self):
        memory = Memory(50.0, Unit.KILO)

        actual = str(memory)
        expected = "50KB"

        assert actual == expected

    def test_float_number_returns_float(self):
        memory = Memory(50.2, Unit.ZETTA)

        actual = str(memory)
        expected = "50.2ZB"

        assert actual == expected


class TestMemoryEquality:
    def test_same_value_and_unit(self):
        value = 50
        unit = Unit.PETA
        mem1 = Memory(value, unit)
        mem2 = Memory(value, unit)

        assert mem1 == mem2

    def test_same_value_different_unit(self):
        value = 50
        unit1 = Unit.PETA
        mem1 = Memory(value, unit1)
        unit2 = Unit.KILO
        mem2 = Memory(value, unit2)

        assert mem1 != mem2

    def test_different_value_same_unit(self):
        value1 = 50
        unit = Unit.PETA
        mem1 = Memory(value1, unit)
        value2 = 60
        mem2 = Memory(value2, unit)

        assert mem1 != mem2

    def test_different_value_different_unit_same_bytes(self):
        mem1 = Memory(500, Unit.MEGA)
        mem2 = Memory(0.5, Unit.GIGA)

        assert mem1 == mem2

    def test_different_value_different_unit_different_bytes(self):
        mem1 = Memory(500, Unit.KILO)
        mem2 = Memory(0.5, Unit.GIGA)

        assert mem1 != mem2


class TestMemoryTo:
    def test_bytes_to_bytes(self):
        memory = Memory(10)
        desired_units = Unit.BYTES

        actual = memory.to(desired_units)
        expected = Memory(10, desired_units)

        assert actual == expected

    def test_bytes_to_kilobytes(self):
        memory = Memory(10)
        desired_units = Unit.KILO

        actual = memory.to(desired_units)
        expected = Memory(0.01, desired_units)

        assert actual == expected

    def test_bytes_to_megabytes(self):
        memory = Memory(2500)
        desired_units = Unit.MEGA

        actual = memory.to(desired_units)
        expected = Memory(0.0025, desired_units)

        assert actual == expected

    def test_kilobytes_to_gigabytes(self):
        memory = Memory(2500, Unit.KILO)
        desired_units = Unit.GIGA

        actual = memory.to(desired_units)
        expected = Memory(0.0025, desired_units)

        assert actual == expected

    def test_terabytes_to_megabytes(self):
        memory = Memory(30, Unit.TERA)
        desired_units = Unit.MEGA

        actual = memory.to(desired_units)
        expected = Memory(30000000, desired_units)

        assert actual == expected

    def test_terabytes_to_kilobytes_in_binary(self):
        memory = Memory(30, Unit.TERA)
        desired_units = Unit.KILO

        actual = memory.to(desired_units, decimal_multiples=False)
        expected = Memory(32212254720, desired_units)

        assert actual == expected


class TestMemoryFromStr:
    def test_empty_string_raises_error(self):
        s = ""

        with pytest.raises(InvalidMemoryString):
            Memory.from_str(s)

    def test_no_suffix_returns_bytes(self):
        s = "500"

        actual = Memory.from_str(s)
        expected = Memory(500)

        assert actual == expected

    def test_no_suffix_and_float_returns_bytes(self):
        s = "500.8"

        actual = Memory.from_str(s)
        expected = Memory(500.8)

        assert actual == expected

    def test_single_letter_suffix_is_valid(self):
        s = "500M"

        actual = Memory.from_str(s)
        expected = Memory(500, Unit.MEGA)

        assert actual == expected

    def test_b_suffix_is_valid(self):
        s = "500MB"

        actual = Memory.from_str(s)
        expected = Memory(500, Unit.MEGA)

        assert actual == expected

    def test_space_between_size_and_suffix_is_valid(self):
        s = "500 MB"

        actual = Memory.from_str(s)
        expected = Memory(500, Unit.MEGA)

        assert actual == expected

    def test_multiple_spaces_between_size_and_suffix_is_valid(self):
        s = "500  MB"

        actual = Memory.from_str(s)
        expected = Memory(500, Unit.MEGA)

        assert actual == expected

    def test_suffix_is_case_insensitive(self):
        s = "500zb"

        actual = Memory.from_str(s).bytes()
        expected = Memory(500, Unit.ZETTA).bytes()

        assert actual == expected

    def test_suffix_only_raises_error(self):
        s = "TB"

        with pytest.raises(InvalidMemoryString):
            Memory.from_str(s)

    def test_bytes_suffix_is_valid(self):
        s = "7B"

        actual = Memory.from_str(s)
        expected = Memory(7)

        assert actual == expected

    def test_invalid_suffix_raises_error(self):
        s = "7LB"

        with pytest.raises(InvalidMemoryString):
            Memory.from_str(s)

    def test_string_with_other_characters_raises_error(self):
        s = "7KBY"

        with pytest.raises(InvalidMemoryString):
            Memory.from_str(s)
