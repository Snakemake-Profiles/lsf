import unittest
from subprocess import CalledProcessError
from unittest.mock import patch

import pytest

from tests.src.OSLayer import OSLayer
from tests.src.lsf_status import StatusChecker, BjobsError, UnknownStatusLine


def assert_called_n_times_with_same_args(mock, n, args):
    assert mock.call_count == n
    for call in mock.call_args_list:
        call_args, _ = call
        assert " ".join(call_args) == args


class Test_LSF_Status_Checker(unittest.TestCase):
    @patch.object(OSLayer, OSLayer.run_process.__name__, return_value=("PEND", ""))
    def test___get_status___bjobs_says_process_is_PEND___job_status_is_running(
        self, run_process_mock
    ):
        lsf_status_checker = StatusChecker(123, "dummy")
        actual = lsf_status_checker.get_status()
        expected = "running"
        self.assertEqual(actual, expected)
        run_process_mock.assert_called_once_with("bjobs -o 'stat' -noheader 123")

    @patch.object(OSLayer, OSLayer.run_process.__name__, return_value=("RUN", ""))
    def test___get_status___bjobs_says_process_is_RUN___job_status_is_running(
        self, run_process_mock
    ):
        lsf_status_checker = StatusChecker(123, "dummy")
        actual = lsf_status_checker.get_status()
        expected = "running"
        self.assertEqual(actual, expected)
        run_process_mock.assert_called_once_with("bjobs -o 'stat' -noheader 123")

    @patch.object(OSLayer, OSLayer.run_process.__name__, return_value=("PSUSP", ""))
    def test___get_status___bjobs_says_process_is_PSUSP___job_status_is_running(
        self, run_process_mock
    ):
        lsf_status_checker = StatusChecker(123, "dummy")
        actual = lsf_status_checker.get_status()
        expected = "running"
        self.assertEqual(actual, expected)
        run_process_mock.assert_called_once_with("bjobs -o 'stat' -noheader 123")

    @patch.object(OSLayer, OSLayer.run_process.__name__, return_value=("USUSP", ""))
    def test___get_status___bjobs_says_process_is_USUSP___job_status_is_running(
        self, run_process_mock
    ):
        lsf_status_checker = StatusChecker(123, "dummy")
        actual = lsf_status_checker.get_status()
        expected = "running"
        self.assertEqual(actual, expected)
        run_process_mock.assert_called_once_with("bjobs -o 'stat' -noheader 123")

    @patch.object(OSLayer, OSLayer.run_process.__name__, return_value=("SSUSP", ""))
    def test___get_status___bjobs_says_process_is_SSUSP___job_status_is_running(
        self, run_process_mock
    ):
        lsf_status_checker = StatusChecker(123, "dummy")
        actual = lsf_status_checker.get_status()
        expected = "running"
        self.assertEqual(actual, expected)
        run_process_mock.assert_called_once_with("bjobs -o 'stat' -noheader 123")

    @patch.object(OSLayer, OSLayer.run_process.__name__, return_value=("WAIT", ""))
    def test___get_status___bjobs_says_process_is_WAIT___job_status_is_running(
        self, run_process_mock
    ):
        lsf_status_checker = StatusChecker(123, "dummy")
        actual = lsf_status_checker.get_status()
        expected = "running"
        self.assertEqual(actual, expected)
        run_process_mock.assert_called_once_with("bjobs -o 'stat' -noheader 123")

    @patch.object(OSLayer, OSLayer.run_process.__name__, return_value=("UNKWN", ""))
    def test___get_status___bjobs_says_process_is_UNKWN___job_status_is_running(
        self, run_process_mock
    ):
        lsf_status_checker = StatusChecker(123, "dummy")
        actual = lsf_status_checker.get_status()
        expected = "running"
        self.assertEqual(actual, expected)
        run_process_mock.assert_called_once_with("bjobs -o 'stat' -noheader 123")

    @patch.object(OSLayer, OSLayer.run_process.__name__, return_value=("EXIT", ""))
    def test___get_status___bjobs_says_process_is_EXIT___job_status_is_failed(
        self, run_process_mock
    ):
        lsf_status_checker = StatusChecker(123, "dummy")
        actual = lsf_status_checker.get_status()
        expected = "failed"
        self.assertEqual(actual, expected)
        run_process_mock.assert_called_once_with("bjobs -o 'stat' -noheader 123")

    @patch.object(OSLayer, OSLayer.run_process.__name__, return_value=("POST_ERR", ""))
    def test___get_status___bjobs_says_process_is_POST_ERR___job_status_is_failed(
        self, run_process_mock
    ):
        lsf_status_checker = StatusChecker(123, "dummy")
        actual = lsf_status_checker.get_status()
        expected = "failed"
        self.assertEqual(actual, expected)
        run_process_mock.assert_called_once_with("bjobs -o 'stat' -noheader 123")

    @patch.object(OSLayer, OSLayer.run_process.__name__, return_value=("DONE", ""))
    def test___get_status___bjobs_says_process_is_DONE___job_status_is_success(
        self, run_process_mock
    ):
        lsf_status_checker = StatusChecker(123, "dummy")
        actual = lsf_status_checker.get_status()
        expected = "success"
        self.assertEqual(actual, expected)
        run_process_mock.assert_called_once_with("bjobs -o 'stat' -noheader 123")

    @patch.object(OSLayer, OSLayer.run_process.__name__, return_value=("POST_DONE", ""))
    def test___get_status___bjobs_says_process_is_POST_DONE___job_status_is_success(
        self, run_process_mock
    ):
        lsf_status_checker = StatusChecker(123, "dummy")
        actual = lsf_status_checker.get_status()
        expected = "success"
        self.assertEqual(actual, expected)
        run_process_mock.assert_called_once_with("bjobs -o 'stat' -noheader 123")

    @patch.object(OSLayer, OSLayer.run_process.__name__)
    def test___get_status___bjobs_fails_three_times_but_says_DONE_in_the_fourth___job_status_is_success(
        self, run_process_mock
    ):
        self.count_fail_three_times_and_then_return_DONE = 0

        def fail_three_times_and_then_return_DONE(cmd):
            self.count_fail_three_times_and_then_return_DONE += 1
            if self.count_fail_three_times_and_then_return_DONE == 1:
                raise BjobsError
            elif self.count_fail_three_times_and_then_return_DONE == 2:
                raise KeyError
            elif self.count_fail_three_times_and_then_return_DONE == 3:
                raise CalledProcessError(1, "bjobs")
            elif self.count_fail_three_times_and_then_return_DONE == 4:
                return "DONE", ""
            else:
                assert False

        run_process_mock.side_effect = fail_three_times_and_then_return_DONE

        lsf_status_checker = StatusChecker(
            123, "dummy", wait_between_tries=0.001, max_status_checks=4
        )
        actual = lsf_status_checker.get_status()
        expected = "success"
        self.assertEqual(actual, expected)
        assert_called_n_times_with_same_args(
            run_process_mock, 4, "bjobs -o 'stat' -noheader 123"
        )

    @patch.object(OSLayer, OSLayer.run_process.__name__)
    def test___get_status___bjobs_fails_three_times_but_says_PEND_in_the_fourth___job_status_is_running(
        self, run_process_mock
    ):
        self.count_fail_three_times_and_then_return_PEND = 0

        def fail_three_times_and_then_return_PEND(cmd):
            self.count_fail_three_times_and_then_return_PEND += 1
            if self.count_fail_three_times_and_then_return_PEND == 1:
                raise BjobsError
            elif self.count_fail_three_times_and_then_return_PEND == 2:
                raise KeyError
            elif self.count_fail_three_times_and_then_return_PEND == 3:
                raise CalledProcessError(1, "bjobs")
            elif self.count_fail_three_times_and_then_return_PEND == 4:
                return "PEND", ""
            else:
                assert False

        run_process_mock.side_effect = fail_three_times_and_then_return_PEND

        lsf_status_checker = StatusChecker(
            123, "dummy", wait_between_tries=0.001, max_status_checks=4
        )
        actual = lsf_status_checker.get_status()
        expected = "running"
        self.assertEqual(actual, expected)
        assert_called_n_times_with_same_args(
            run_process_mock, 4, "bjobs -o 'stat' -noheader 123"
        )

    @patch.object(OSLayer, OSLayer.run_process.__name__)
    def test___get_status___bjobs_fails_one_but_says_EXIT_in_the_fourth___job_status_is_failed(
        self, run_process_mock
    ):
        self.count_fail_three_times_and_then_return_FAIL = 0

        def fail_one_time_and_then_return_FAIL(cmd):
            self.count_fail_three_times_and_then_return_FAIL += 1
            if self.count_fail_three_times_and_then_return_FAIL == 1:
                raise BjobsError
            elif self.count_fail_three_times_and_then_return_FAIL == 2:
                return "EXIT", ""
            else:
                assert False

        run_process_mock.side_effect = fail_one_time_and_then_return_FAIL

        lsf_status_checker = StatusChecker(
            123, "dummy", wait_between_tries=0.001, max_status_checks=4
        )
        actual = lsf_status_checker.get_status()
        expected = "failed"
        self.assertEqual(actual, expected)
        assert_called_n_times_with_same_args(
            run_process_mock, 2, "bjobs -o 'stat' -noheader 123"
        )

    @patch.object(OSLayer, OSLayer.run_process.__name__, side_effect=BjobsError)
    @patch.object(
        StatusChecker,
        StatusChecker._get_tail_of_log_file.__name__,
        return_value=["Successfully completed.", "", "Resource usage summary:"],
    )
    def test___get_status___bjobs_fails_all_times___query_status_using_log___job_status_is_success(
        self, get_lines_of_log_file_mock, run_process_mock
    ):
        lsf_status_checker = StatusChecker(
            123, "dummy", wait_between_tries=0.001, max_status_checks=4
        )
        actual = lsf_status_checker.get_status()
        expected = "success"
        self.assertEqual(actual, expected)
        assert_called_n_times_with_same_args(
            run_process_mock, 4, "bjobs -o 'stat' -noheader 123"
        )
        get_lines_of_log_file_mock.assert_called_once_with()

    @patch.object(OSLayer, OSLayer.run_process.__name__, side_effect=BjobsError)
    @patch.object(
        StatusChecker,
        StatusChecker._get_tail_of_log_file.__name__,
        return_value=["Exited with exit code 1.", "", "Resource usage summary:"],
    )
    def test___get_status___bjobs_fails_all_times___query_status_using_log___job_status_is_failed(
        self, get_lines_of_log_file_mock, run_process_mock
    ):
        lsf_status_checker = StatusChecker(
            123, "dummy", wait_between_tries=0.001, max_status_checks=4
        )
        actual = lsf_status_checker.get_status()
        expected = "failed"
        self.assertEqual(actual, expected)
        assert_called_n_times_with_same_args(
            run_process_mock, 4, "bjobs -o 'stat' -noheader 123"
        )
        get_lines_of_log_file_mock.assert_called_once_with()

    @patch.object(OSLayer, OSLayer.run_process.__name__, side_effect=BjobsError)
    @patch.object(
        StatusChecker,
        StatusChecker._get_tail_of_log_file.__name__,
        side_effect=FileNotFoundError,
    )
    def test___get_status___bjobs_fails_all_times___query_status_using_log___log_file_does_not_yet_exists___job_status_is_running(
        self, get_lines_of_log_file_mock, run_process_mock
    ):
        lsf_status_checker = StatusChecker(
            123, "dummy", wait_between_tries=0.001, max_status_checks=4
        )
        actual = lsf_status_checker.get_status()
        expected = "running"
        self.assertEqual(actual, expected)
        assert_called_n_times_with_same_args(
            run_process_mock, 4, "bjobs -o 'stat' -noheader 123"
        )
        get_lines_of_log_file_mock.assert_called_once_with()

    @patch.object(OSLayer, OSLayer.run_process.__name__, side_effect=BjobsError)
    @patch.object(
        StatusChecker,
        StatusChecker._get_tail_of_log_file.__name__,
        return_value=["...", "..."],
    )
    def test___get_status___bjobs_fails_all_times___query_status_using_log___log_file_exists_but_exit_info_not_yet_written___job_status_is_running(
        self, get_lines_of_log_file_mock, run_process_mock
    ):
        lsf_status_checker = StatusChecker(
            123, "dummy", wait_between_tries=0.001, max_status_checks=4
        )
        actual = lsf_status_checker.get_status()
        expected = "running"
        self.assertEqual(actual, expected)
        assert_called_n_times_with_same_args(
            run_process_mock, 4, "bjobs -o 'stat' -noheader 123"
        )
        get_lines_of_log_file_mock.assert_called_once_with()

    @patch.object(OSLayer, OSLayer.run_process.__name__, side_effect=BjobsError)
    @patch.object(
        StatusChecker,
        StatusChecker._get_tail_of_log_file.__name__,
        return_value=["Successfully completed.", ""],
    )
    def test___get_status___bjobs_fails_all_times___query_status_using_log___log_file_exists_but_resource_line_does_not_exist___job_status_is_running(
        self, get_lines_of_log_file_mock, run_process_mock
    ):
        lsf_status_checker = StatusChecker(
            123, "dummy", wait_between_tries=0.001, max_status_checks=4
        )
        actual = lsf_status_checker.get_status()
        expected = "running"
        self.assertEqual(actual, expected)
        assert_called_n_times_with_same_args(
            run_process_mock, 4, "bjobs -o 'stat' -noheader 123"
        )
        get_lines_of_log_file_mock.assert_called_once_with()

    @patch.object(OSLayer, OSLayer.run_process.__name__, side_effect=BjobsError)
    @patch.object(
        StatusChecker,
        StatusChecker._get_tail_of_log_file.__name__,
        return_value=["I am an unknown status line", "", "Resource usage summary:"],
    )
    def test___get_status___bjobs_fails_all_times___query_status_using_log___log_file_exists_but_resource_line_is_not_recognised___job_status_is_running(
        self, get_lines_of_log_file_mock, run_process_mock
    ):
        lsf_status_checker = StatusChecker(
            123, "dummy", wait_between_tries=0.001, max_status_checks=4
        )
        with pytest.raises(UnknownStatusLine) as err:
            lsf_status_checker.get_status()

        assert err.match("I am an unknown status line")
        assert_called_n_times_with_same_args(
            run_process_mock, 4, "bjobs -o 'stat' -noheader 123"
        )
        get_lines_of_log_file_mock.assert_called_once_with()

    @patch.object(OSLayer, OSLayer.run_process.__name__, return_value=("", ""))
    def test____query_status_using_bjobs___empty_stdout___raises_BjobsError(
        self, run_process_mock
    ):
        lsf_status_checker = StatusChecker(
            123, "dummy", wait_between_tries=0.001, max_status_checks=4
        )
        self.assertRaises(BjobsError, lsf_status_checker._query_status_using_bjobs)
        run_process_mock.assert_called_once_with("bjobs -o 'stat' -noheader 123")

    @patch.object(OSLayer, OSLayer.run_process.__name__, return_value=("asd", ""))
    def test____query_status_using_bjobs___unknown_job_status___raises_KeyError(
        self, run_process_mock
    ):
        lsf_status_checker = StatusChecker(
            123, "dummy", wait_between_tries=0.001, max_status_checks=4
        )
        self.assertRaises(KeyError, lsf_status_checker._query_status_using_bjobs)
        run_process_mock.assert_called_once_with("bjobs -o 'stat' -noheader 123")

    def test____get_tail_of_log_file(self):
        lsf_status_checker = StatusChecker(
            123, "test_file.txt", wait_between_tries=0.001, max_status_checks=4
        )
        actual = lsf_status_checker._get_tail_of_log_file()
        expected = ["abcd", "1234"]
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
