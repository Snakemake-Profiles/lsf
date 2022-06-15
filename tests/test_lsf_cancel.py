import unittest
from unittest.mock import patch

from tests.src.OSLayer import OSLayer
from tests.src.lsf_cancel import kill_jobs, parse_input, KILL


class TestParseInput(unittest.TestCase):
    script = "lsf_cancel.py"

    def test_parse_input_no_args(self):
        fake_args = [self.script]
        with patch("sys.argv", fake_args):
            actual = parse_input()

        assert not actual

    def test_parse_input_one_job_no_log(self):
        fake_args = [self.script, "1234"]
        with patch("sys.argv", fake_args):
            actual = parse_input()

        expected = fake_args[1:]
        assert actual == expected

    def test_parse_input_one_job_and_log(self):
        fake_args = [self.script, "1234", "log/file.out"]
        with patch("sys.argv", fake_args):
            actual = parse_input()

        expected = [fake_args[1]]
        assert actual == expected

    def test_parse_input_two_jobs_and_log(self):
        fake_args = [self.script, "1234", "log/file.out", "9090", "log/other.out"]
        with patch("sys.argv", fake_args):
            actual = parse_input()

        expected = [fake_args[1], fake_args[3]]
        assert actual == expected

    def test_parse_input_two_jobs_and_digits_in_log(self):
        fake_args = [self.script, "1234", "log/file.out", "9090", "log/123"]
        with patch("sys.argv", fake_args):
            actual = parse_input()

        expected = [fake_args[1], fake_args[3]]
        assert actual == expected

    def test_parse_input_multiple_args_but_no_jobs(self):
        fake_args = [self.script, "log/file.out", "log/123"]
        with patch("sys.argv", fake_args):
            actual = parse_input()

        assert not actual


class TestKillJobs(unittest.TestCase):
    @patch.object(
        OSLayer,
        OSLayer.run_process.__name__,
        return_value=(
            "Job <123> is being terminated",
            "",
        ),
    )
    def test_kill_jobs_one_job(
        self,
        run_process_mock,
    ):
        jobids = ["123"]
        expected_kill_cmd = "{} {}".format(KILL, " ".join(jobids))

        kill_jobs(jobids)

        run_process_mock.assert_called_once_with(expected_kill_cmd, check=False)

    @patch.object(
        OSLayer,
        OSLayer.run_process.__name__,
        return_value=(
            "Job <123> is being terminated\nJob <456> is being terminated",
            "",
        ),
    )
    def test_kill_jobs_two_jobs(
        self,
        run_process_mock,
    ):
        jobids = ["123", "456"]
        expected_kill_cmd = "{} {}".format(KILL, " ".join(jobids))

        kill_jobs(jobids)

        run_process_mock.assert_called_once_with(expected_kill_cmd, check=False)

    @patch.object(
        OSLayer,
        OSLayer.run_process.__name__,
        return_value=("", ""),
    )
    def test_kill_jobs_no_jobs(
        self,
        run_process_mock,
    ):
        jobids = []

        kill_jobs(jobids)

        run_process_mock.assert_not_called()

    @patch.object(
        OSLayer,
        OSLayer.run_process.__name__,
        return_value=("", ""),
    )
    def test_kill_jobs_empty_jobs(self, run_process_mock):
        jobids = ["", ""]

        kill_jobs(jobids)

        run_process_mock.assert_not_called()

    @patch.object(
        OSLayer,
        OSLayer.run_process.__name__,
        return_value=("", ""),
    )
    def test_kill_jobs_empty_job_and_non_empty_job(self, run_process_mock):
        jobids = ["", "123"]

        expected_kill_cmd = "{} {}".format(KILL, " ".join(jobids))

        kill_jobs(jobids)

        run_process_mock.assert_called_once_with(expected_kill_cmd, check=False)
