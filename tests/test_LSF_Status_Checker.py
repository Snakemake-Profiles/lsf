import unittest
from unittest.mock import Mock, patch
from tests.src.lsf_status import LSF_Status_Checker, BjobsError
from tests.src.OSLayer import OSLayer
from subprocess import CalledProcessError

count_fail_three_times_and_then_return_DONE=0
count_fail_three_times_and_then_return_PEND=0
count_fail_three_times_and_then_return_FAIL=0

class Test_LSF_Status_Checker(unittest.TestCase):
    @patch.object(OSLayer, OSLayer.run_process_and_get_output_and_error_stream.__name__, return_value=("PEND", ""))
    def test___get_status___bjobs_says_process_is_PEND___job_status_is_running(self, run_process_and_get_output_and_error_stream_mock):
        lsf_status_checker = LSF_Status_Checker(123, "dummy")
        actual = lsf_status_checker.get_status()
        expected = "running"
        self.assertEqual(actual, expected)
        run_process_and_get_output_and_error_stream_mock.assert_called_once_with("bjobs -o 'stat' -noheader 123")

    @patch.object(OSLayer, OSLayer.run_process_and_get_output_and_error_stream.__name__, return_value=("RUN", ""))
    def test___get_status___bjobs_says_process_is_RUN___job_status_is_running(self, run_process_and_get_output_and_error_stream_mock):
        lsf_status_checker = LSF_Status_Checker(123, "dummy")
        actual = lsf_status_checker.get_status()
        expected = "running"
        self.assertEqual(actual, expected)
        run_process_and_get_output_and_error_stream_mock.assert_called_once_with("bjobs -o 'stat' -noheader 123")

    @patch.object(OSLayer, OSLayer.run_process_and_get_output_and_error_stream.__name__, return_value=("PSUSP", ""))
    def test___get_status___bjobs_says_process_is_PSUSP___job_status_is_running(self, run_process_and_get_output_and_error_stream_mock):
        lsf_status_checker = LSF_Status_Checker(123, "dummy")
        actual = lsf_status_checker.get_status()
        expected = "running"
        self.assertEqual(actual, expected)
        run_process_and_get_output_and_error_stream_mock.assert_called_once_with("bjobs -o 'stat' -noheader 123")


    @patch.object(OSLayer, OSLayer.run_process_and_get_output_and_error_stream.__name__, return_value=("USUSP", ""))
    def test___get_status___bjobs_says_process_is_USUSP___job_status_is_running(self, run_process_and_get_output_and_error_stream_mock):
        lsf_status_checker = LSF_Status_Checker(123, "dummy")
        actual = lsf_status_checker.get_status()
        expected = "running"
        self.assertEqual(actual, expected)
        run_process_and_get_output_and_error_stream_mock.assert_called_once_with("bjobs -o 'stat' -noheader 123")


    @patch.object(OSLayer, OSLayer.run_process_and_get_output_and_error_stream.__name__, return_value=("SSUSP", ""))
    def test___get_status___bjobs_says_process_is_SSUSP___job_status_is_running(self, run_process_and_get_output_and_error_stream_mock):
        lsf_status_checker = LSF_Status_Checker(123, "dummy")
        actual = lsf_status_checker.get_status()
        expected = "running"
        self.assertEqual(actual, expected)
        run_process_and_get_output_and_error_stream_mock.assert_called_once_with("bjobs -o 'stat' -noheader 123")


    @patch.object(OSLayer, OSLayer.run_process_and_get_output_and_error_stream.__name__, return_value=("WAIT", ""))
    def test___get_status___bjobs_says_process_is_WAIT___job_status_is_running(self, run_process_and_get_output_and_error_stream_mock):
        lsf_status_checker = LSF_Status_Checker(123, "dummy")
        actual = lsf_status_checker.get_status()
        expected = "running"
        self.assertEqual(actual, expected)
        run_process_and_get_output_and_error_stream_mock.assert_called_once_with("bjobs -o 'stat' -noheader 123")


    @patch.object(OSLayer, OSLayer.run_process_and_get_output_and_error_stream.__name__, return_value=("UNKWN", ""))
    def test___get_status___bjobs_says_process_is_UNKWN___job_status_is_running(self, run_process_and_get_output_and_error_stream_mock):
        lsf_status_checker = LSF_Status_Checker(123, "dummy")
        actual = lsf_status_checker.get_status()
        expected = "running"
        self.assertEqual(actual, expected)
        run_process_and_get_output_and_error_stream_mock.assert_called_once_with("bjobs -o 'stat' -noheader 123")

    @patch.object(OSLayer, OSLayer.run_process_and_get_output_and_error_stream.__name__, return_value=("EXIT", ""))
    def test___get_status___bjobs_says_process_is_EXIT___job_status_is_failed(self, run_process_and_get_output_and_error_stream_mock):
        lsf_status_checker = LSF_Status_Checker(123, "dummy")
        actual = lsf_status_checker.get_status()
        expected = "failed"
        self.assertEqual(actual, expected)
        run_process_and_get_output_and_error_stream_mock.assert_called_once_with("bjobs -o 'stat' -noheader 123")

    @patch.object(OSLayer, OSLayer.run_process_and_get_output_and_error_stream.__name__, return_value=("POST_ERR", ""))
    def test___get_status___bjobs_says_process_is_POST_ERR___job_status_is_failed(self,
                                                                              run_process_and_get_output_and_error_stream_mock):
        lsf_status_checker = LSF_Status_Checker(123, "dummy")
        actual = lsf_status_checker.get_status()
        expected = "failed"
        self.assertEqual(actual, expected)
        run_process_and_get_output_and_error_stream_mock.assert_called_once_with("bjobs -o 'stat' -noheader 123")

    @patch.object(OSLayer, OSLayer.run_process_and_get_output_and_error_stream.__name__, return_value=("DONE", ""))
    def test___get_status___bjobs_says_process_is_DONE___job_status_is_success(self,
                                                                                  run_process_and_get_output_and_error_stream_mock):
        lsf_status_checker = LSF_Status_Checker(123, "dummy")
        actual = lsf_status_checker.get_status()
        expected = "success"
        self.assertEqual(actual, expected)
        run_process_and_get_output_and_error_stream_mock.assert_called_once_with("bjobs -o 'stat' -noheader 123")

    @patch.object(OSLayer, OSLayer.run_process_and_get_output_and_error_stream.__name__, return_value=("POST_DONE", ""))
    def test___get_status___bjobs_says_process_is_POST_DONE___job_status_is_success(self,
                                                                                  run_process_and_get_output_and_error_stream_mock):
        lsf_status_checker = LSF_Status_Checker(123, "dummy")
        actual = lsf_status_checker.get_status()
        expected = "success"
        self.assertEqual(actual, expected)
        run_process_and_get_output_and_error_stream_mock.assert_called_once_with("bjobs -o 'stat' -noheader 123")

    @patch.object(OSLayer, OSLayer.run_process_and_get_output_and_error_stream.__name__)
    def test___get_status___bjobs_fails_three_times_but_works_on_the_last___job_status_is_success(self,
                                                                                    run_process_and_get_output_and_error_stream_mock):
        def fail_three_times_and_then_return_DONE(cmd):
            global count_fail_three_times_and_then_return_DONE
            count_fail_three_times_and_then_return_DONE += 1
            if count_fail_three_times_and_then_return_DONE == 1:
                raise BjobsError
            elif count_fail_three_times_and_then_return_DONE == 2:
                raise KeyError
            elif count_fail_three_times_and_then_return_DONE == 3:
                raise CalledProcessError(1, "bjobs")
            elif count_fail_three_times_and_then_return_DONE == 4:
                return "DONE", ""
            else:
                assert False

        run_process_and_get_output_and_error_stream_mock.side_effect = fail_three_times_and_then_return_DONE

        lsf_status_checker = LSF_Status_Checker(123, "dummy", WAIT_BETWEEN_TRIES=0.1, TRY_TIMES=4)
        actual = lsf_status_checker.get_status()
        expected = "success"
        self.assertEqual(actual, expected)
        for call in run_process_and_get_output_and_error_stream_mock.call_args_list:
            args, kwargs = call
            self.assertEqual(" ".join(args), "bjobs -o 'stat' -noheader 123")


    @patch.object(OSLayer, OSLayer.run_process_and_get_output_and_error_stream.__name__)
    def test___get_status___bjobs_fails_three_times_but_bjobs_says_PEND_on_the_last___job_status_is_running(self,
                                                                                    run_process_and_get_output_and_error_stream_mock):
        def fail_three_times_and_then_return_PEND(cmd):
            global count_fail_three_times_and_then_return_PEND
            count_fail_three_times_and_then_return_PEND += 1
            if count_fail_three_times_and_then_return_PEND == 1:
                raise BjobsError
            elif count_fail_three_times_and_then_return_PEND == 2:
                raise KeyError
            elif count_fail_three_times_and_then_return_PEND == 3:
                raise CalledProcessError(1, "bjobs")
            elif count_fail_three_times_and_then_return_PEND == 4:
                return "PEND", ""
            else:
                assert False

        run_process_and_get_output_and_error_stream_mock.side_effect = fail_three_times_and_then_return_PEND

        lsf_status_checker = LSF_Status_Checker(123, "dummy", WAIT_BETWEEN_TRIES=0.1, TRY_TIMES=4)
        actual = lsf_status_checker.get_status()
        expected = "running"
        self.assertEqual(actual, expected)
        for call in run_process_and_get_output_and_error_stream_mock.call_args_list:
            args, kwargs = call
            self.assertEqual(" ".join(args), "bjobs -o 'stat' -noheader 123")

    @patch.object(OSLayer, OSLayer.run_process_and_get_output_and_error_stream.__name__)
    def test___get_status___bjobs_fails_one_but_bjobs_says_EXIT_on_the_last___job_status_is_failed(self,
                                                                                                            run_process_and_get_output_and_error_stream_mock):
        def fail_one_time_and_then_return_FAIL(cmd):
            global count_fail_three_times_and_then_return_FAIL
            count_fail_three_times_and_then_return_FAIL += 1
            if count_fail_three_times_and_then_return_FAIL == 1:
                raise BjobsError
            elif count_fail_three_times_and_then_return_FAIL == 2:
                return "EXIT", ""
            else:
                assert False

        run_process_and_get_output_and_error_stream_mock.side_effect = fail_one_time_and_then_return_FAIL

        lsf_status_checker = LSF_Status_Checker(123, "dummy", WAIT_BETWEEN_TRIES=0.1, TRY_TIMES=4)
        actual = lsf_status_checker.get_status()
        expected = "failed"
        self.assertEqual(actual, expected)
        for call in run_process_and_get_output_and_error_stream_mock.call_args_list:
            args, kwargs = call
            self.assertEqual(" ".join(args), "bjobs -o 'stat' -noheader 123")











    @patch.object(OSLayer, OSLayer.run_process_and_get_output_and_error_stream.__name__, return_value=("",""))
    def test____query_status_using_bjobs___empty_stdout___raises_BjobsError(self, run_process_and_get_output_and_error_stream_mock):
        lsf_status_checker = LSF_Status_Checker(123, "dummy", WAIT_BETWEEN_TRIES=0.1, TRY_TIMES=4)
        self.assertRaises(BjobsError, lsf_status_checker._query_status_using_bjobs)
        run_process_and_get_output_and_error_stream_mock.assert_called_once_with("bjobs -o 'stat' -noheader 123")

    @patch.object(OSLayer, OSLayer.run_process_and_get_output_and_error_stream.__name__, return_value=("asd", ""))
    def test____query_status_using_bjobs___unknown_job_status___raises_KeyError(self,
                                                                            run_process_and_get_output_and_error_stream_mock):
        lsf_status_checker = LSF_Status_Checker(123, "dummy", WAIT_BETWEEN_TRIES=0.1, TRY_TIMES=4)
        self.assertRaises(KeyError, lsf_status_checker._query_status_using_bjobs)
        run_process_and_get_output_and_error_stream_mock.assert_called_once_with("bjobs -o 'stat' -noheader 123")

if __name__ == '__main__':
    unittest.main()