import unittest
from pathlib import Path
from subprocess import CalledProcessError
from unittest.mock import patch

from tests.src.CookieCutter import CookieCutter
from tests.src.OSLayer import OSLayer
from tests.src.lsf_submit import (
    Submitter,
    BsubInvocationError,
    JobidNotFoundError,
    MemoryUnits,
)


class TestSubmitter(unittest.TestCase):
    @patch.object(
        CookieCutter, CookieCutter.get_log_dir.__name__, return_value="logdir"
    )
    @patch.object(
        CookieCutter, CookieCutter.get_default_mem_mb.__name__, return_value=1000
    )
    @patch.object(
        CookieCutter, CookieCutter.get_default_threads.__name__, return_value=8
    )
    @patch.object(OSLayer, OSLayer.get_uuid4_string.__name__, return_value="random")
    def test___several_trivial_getter_methods(self, *mocks):
        argv = [
            "script_name",
            "cluster_opt_1",
            "cluster_opt_2",
            "cluster_opt_3",
            "real_jobscript.sh",
        ]
        memory_units = MemoryUnits.GB
        lsf_submit = Submitter(argv, memory_units=memory_units)
        self.assertEqual(lsf_submit.jobscript, "real_jobscript.sh")
        self.assertEqual(
            lsf_submit.cluster_cmd, "cluster_opt_1 cluster_opt_2 cluster_opt_3"
        )
        self.assertEqual(lsf_submit.threads, 1)
        self.assertEqual(lsf_submit.mem_mb, 2662)
        self.assertEqual(lsf_submit.jobid, 2)
        self.assertEqual(lsf_submit.wildcards_str, "i=0")
        self.assertEqual(lsf_submit.rule_name, "search_fasta_on_index")
        self.assertEqual(lsf_submit.is_group_jobtype, False)
        expected_mem = "2662GB"
        self.assertEqual(
            lsf_submit.resources_cmd,
            "-M {mem} -n 1 -R 'select[mem>{mem}] rusage[mem={mem}] span[hosts=1]'".format(
                mem=expected_mem
            ),
        )
        self.assertEqual(lsf_submit.jobname, "search_fasta_on_index.i=0")
        self.assertEqual(lsf_submit.logdir, Path("logdir"))
        self.assertEqual(lsf_submit.outlog, Path("logdir") / "2_random.out")
        self.assertEqual(lsf_submit.errlog, Path("logdir") / "2_random.err")
        self.assertEqual(
            lsf_submit.jobinfo_cmd,
            '-o "logdir/2_random.out" -e "logdir/2_random.err" -J "search_fasta_on_index.i=0"',
        )
        self.assertEqual(lsf_submit.queue_cmd, "-q q1")
        self.assertEqual(
            lsf_submit.submit_cmd,
            "bsub -M {mem} -n 1 -R 'select[mem>{mem}] rusage[mem={mem}] span[hosts=1]' "
            '-o "logdir/2_random.out" -e "logdir/2_random.err" -J "search_fasta_on_index.i=0" '
            "-q q1 "
            "cluster_opt_1 cluster_opt_2 cluster_opt_3 "
            "real_jobscript.sh".format(mem=expected_mem),
        )

    @patch.object(
        OSLayer,
        OSLayer.run_process.__name__,
        return_value=(
            "Job <8697223> is submitted to default queue <research-rh74>. logs/cluster/2_z137TAmCoQGdWHohm5m2zHH5E5MWxmTUJTdU1Uj3iqKVILs4n3R37nruIEJBcQoi.out",
            "",
        ),
    )
    @patch.object(
        CookieCutter, CookieCutter.get_log_dir.__name__, return_value="logdir"
    )
    @patch.object(
        CookieCutter, CookieCutter.get_default_mem_mb.__name__, return_value=1000
    )
    @patch.object(
        CookieCutter, CookieCutter.get_default_threads.__name__, return_value=8
    )
    @patch.object(OSLayer, OSLayer.get_uuid4_string.__name__, return_value="random")
    def test____submit_cmd_and_get_external_job_id___real_output_stream_from_submission(
        self, *mocks
    ):
        argv = [
            "script_name",
            "cluster_opt_1",
            "cluster_opt_2",
            "cluster_opt_3",
            "real_jobscript.sh",
        ]
        lsf_submit = Submitter(argv)
        actual = lsf_submit._submit_cmd_and_get_external_job_id()
        expected = 8697223
        self.assertEqual(actual, expected)

    @patch.object(OSLayer, OSLayer.run_process.__name__, return_value=("", ""))
    @patch.object(
        CookieCutter, CookieCutter.get_log_dir.__name__, return_value="logdir"
    )
    @patch.object(
        CookieCutter, CookieCutter.get_default_mem_mb.__name__, return_value=1000
    )
    @patch.object(
        CookieCutter, CookieCutter.get_default_threads.__name__, return_value=8
    )
    @patch.object(OSLayer, OSLayer.get_uuid4_string.__name__, return_value="random")
    def test____submit_cmd_and_get_external_job_id___output_stream_has_no_jobid(
        self, *mocks
    ):
        argv = [
            "script_name",
            "cluster_opt_1",
            "cluster_opt_2",
            "cluster_opt_3",
            "real_jobscript.sh",
        ]
        lsf_submit = Submitter(argv)
        self.assertRaises(JobidNotFoundError, lsf_submit.submit)

    @patch.object(
        CookieCutter, CookieCutter.get_log_dir.__name__, return_value="logdir"
    )
    @patch.object(
        CookieCutter, CookieCutter.get_default_mem_mb.__name__, return_value=1000
    )
    @patch.object(
        CookieCutter, CookieCutter.get_default_threads.__name__, return_value=8
    )
    @patch.object(OSLayer, OSLayer.get_uuid4_string.__name__, return_value="random")
    @patch.object(OSLayer, OSLayer.mkdir.__name__)
    @patch.object(OSLayer, OSLayer.remove_file.__name__)
    @patch.object(
        OSLayer,
        OSLayer.run_process.__name__,
        return_value=(
            "Job <123456> is submitted to default queue <research-rh74>.",
            "",
        ),
    )
    @patch.object(OSLayer, OSLayer.print.__name__)
    def test___submit___successfull_submit(
        self,
        print_mock,
        run_process_mock,
        remove_file_mock,
        mkdir_mock,
        *uninteresting_mocks
    ):
        argv = [
            "script_name",
            "cluster_opt_1",
            "cluster_opt_2",
            "cluster_opt_3",
            "real_jobscript.sh",
        ]
        mem_units = MemoryUnits.MB
        lsf_submit = Submitter(argv, memory_units=mem_units)

        lsf_submit.submit()

        mkdir_mock.assert_called_once_with(Path("logdir"))
        self.assertEqual(remove_file_mock.call_count, 2)
        remove_file_mock.assert_any_call(Path("logdir/2_random.out"))
        remove_file_mock.assert_any_call(Path("logdir/2_random.err"))
        expected_mem = "2662{}".format(mem_units.value)
        run_process_mock.assert_called_once_with(
            "bsub -M {mem} -n 1 -R 'select[mem>{mem}] rusage[mem={mem}] span[hosts=1]' "
            '-o "logdir/2_random.out" -e "logdir/2_random.err" -J "search_fasta_on_index.i=0" '
            "-q q1 "
            "cluster_opt_1 cluster_opt_2 cluster_opt_3 "
            "real_jobscript.sh".format(mem=expected_mem)
        )
        print_mock.assert_called_once_with("123456 logdir/2_random.out")

    @patch.object(
        CookieCutter, CookieCutter.get_log_dir.__name__, return_value="logdir"
    )
    @patch.object(
        CookieCutter, CookieCutter.get_default_mem_mb.__name__, return_value=1000
    )
    @patch.object(
        CookieCutter, CookieCutter.get_default_threads.__name__, return_value=8
    )
    @patch.object(OSLayer, OSLayer.get_uuid4_string.__name__, return_value="random")
    @patch.object(OSLayer, OSLayer.mkdir.__name__)
    @patch.object(OSLayer, OSLayer.remove_file.__name__)
    @patch.object(
        OSLayer, OSLayer.run_process.__name__, side_effect=CalledProcessError(1, "bsub")
    )
    @patch.object(OSLayer, OSLayer.print.__name__)
    def test___submit___failed_submit_bsub_invocation_error(
        self,
        print_mock,
        run_process_mock,
        remove_file_mock,
        mkdir_mock,
        *uninteresting_mocks
    ):
        argv = [
            "script_name",
            "cluster_opt_1",
            "cluster_opt_2",
            "cluster_opt_3",
            "real_jobscript.sh",
        ]
        lsf_submit = Submitter(argv)

        self.assertRaises(BsubInvocationError, lsf_submit.submit)

        mkdir_mock.assert_called_once_with(Path("logdir"))
        self.assertEqual(remove_file_mock.call_count, 2)
        remove_file_mock.assert_any_call(Path("logdir/2_random.out"))
        remove_file_mock.assert_any_call(Path("logdir/2_random.err"))
        expected_mem = "2662KB"
        run_process_mock.assert_called_once_with(
            "bsub -M {mem} -n 1 -R 'select[mem>{mem}] rusage[mem={mem}] span[hosts=1]' "
            '-o "logdir/2_random.out" -e "logdir/2_random.err" -J "search_fasta_on_index.i=0" '
            "-q q1 "
            "cluster_opt_1 cluster_opt_2 cluster_opt_3 "
            "real_jobscript.sh".format(mem=expected_mem)
        )
        print_mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
