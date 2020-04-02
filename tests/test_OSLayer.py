import pytest

from tests.src.OSLayer import OSLayer, TailError


class TestTail:
    def test_emptyFile_returnsEmpty(self, tmpdir):
        content = ""
        path = tmpdir.join("tail.txt")
        path.write(content)

        actual = OSLayer.tail(str(path))

        assert not actual

    def test_nonExistentFile_raisesError(self):
        path = "foo.bar"
        with pytest.raises(TailError) as err:
            OSLayer.tail(path)

        assert err.match("No such file")

    def test_oneLineInFile_returnsLine(self, tmpdir):
        content = "one line\n"
        path = tmpdir.join("tail.txt")
        path.write(content)

        actual = OSLayer.tail(str(path))
        expected = [b"one line\n"]

        assert actual == expected

    def test_twoLinesInFile_returnsLines(self, tmpdir):
        content = "one line\nsecond line\n"
        path = tmpdir.join("tail.txt")
        path.write(content)

        actual = OSLayer.tail(str(path))
        expected = [b"one line\n", b"second line\n"]

        assert actual == expected

    def test_moreLinesInFileThanRequestedNumber_returnsLastNLines(self, tmpdir):
        content = "one line\nsecond line\nthird line\n"
        path = tmpdir.join("tail.txt")
        path.write(content)
        n = 2

        actual = OSLayer.tail(str(path), num_lines=n)
        expected = [b"second line\n", b"third line\n"]

        assert actual == expected
