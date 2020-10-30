from unittest.mock import patch

import pytest

from tests.src.CookieCutter import CookieCutter
from tests.src.OSLayer import OSLayer, TailError


class TestTail:
    def test_emptyFile_returnsEmpty(self, tmpdir):
        content = ""
        path = tmpdir.join("tail.txt")
        path.write(content)

        actual = OSLayer.tail(str(path))

        assert not actual

    @patch.object(
        CookieCutter, CookieCutter.get_latency_wait.__name__, return_value=0.5
    )
    def test_nonExistentFile_raisesError(self, *mocks):
        path = "foo.bar"
        with pytest.raises(FileNotFoundError) as err:
            OSLayer.tail(path)

        assert err.match("{} does not exist".format(path))

    def test_numLinesIsNotInt_raisesError(self, tmpdir):
        path = str(tmpdir)
        with pytest.raises(TailError):
            OSLayer.tail(path, num_lines=3.3)

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
