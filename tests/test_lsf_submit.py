import unittest
from io import StringIO
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
from tests.src.lsf_config import Config


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
        jobscript = argv[-1]
        cluster_cmds = argv[1:-1]
        lsf_submit = Submitter(
            jobscript=jobscript, cluster_cmds=cluster_cmds, memory_units=memory_units
        )
        self.assertEqual(lsf_submit.jobscript, "real_jobscript.sh")
        self.assertEqual(
            lsf_submit.cluster_cmd, "cluster_opt_1 cluster_opt_2 cluster_opt_3"
        )
        self.assertEqual(lsf_submit.threads, 1)
        self.assertEqual(lsf_submit.mem_mb, 2662)
        self.assertEqual(lsf_submit.jobid, 2)
        expected_wildcards_str = "i=0"
        self.assertEqual(lsf_submit.wildcards_str, expected_wildcards_str)
        expected_rule_name = "search_fasta_on_index"
        self.assertEqual(lsf_submit.rule_name, expected_rule_name)
        self.assertEqual(lsf_submit.is_group_jobtype, False)
        expected_mem = "2662GB"
        self.assertEqual(
            lsf_submit.resources_cmd,
            "-M {mem} -n 1 -R 'select[mem>{mem}] rusage[mem={mem}] span[hosts=1]'".format(
                mem=expected_mem
            ),
        )
        self.assertEqual(lsf_submit.jobname, "search_fasta_on_index.i=0")
        expected_logdir = Path("logdir") / expected_rule_name / expected_wildcards_str
        self.assertEqual(lsf_submit.logdir, expected_logdir)
        expected_outlog = expected_logdir / "jobid2_random.out"
        self.assertEqual(lsf_submit.outlog, expected_outlog)
        expected_errlog = expected_logdir / "jobid2_random.err"
        self.assertEqual(lsf_submit.errlog, expected_errlog)
        expected_jobinfo_cmd = '-o "{outlog}" -e "{errlog}" -J "search_fasta_on_index.i=0"'.format(
            outlog=expected_outlog, errlog=expected_errlog
        )
        self.assertEqual(
            lsf_submit.jobinfo_cmd, expected_jobinfo_cmd,
        )
        self.assertEqual(lsf_submit.queue_cmd, "-q q1")
        self.assertEqual(
            lsf_submit.submit_cmd,
            "bsub -M {mem} -n 1 -R 'select[mem>{mem}] rusage[mem={mem}] span[hosts=1]' "
            "{jobinfo} -q q1 cluster_opt_1 cluster_opt_2 cluster_opt_3 "
            "real_jobscript.sh".format(mem=expected_mem, jobinfo=expected_jobinfo_cmd),
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
        jobscript = argv[-1]
        cluster_cmds = argv[1:-1]
        lsf_submit = Submitter(jobscript=jobscript, cluster_cmds=cluster_cmds)
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
        jobscript = argv[-1]
        cluster_cmds = argv[1:-1]
        lsf_submit = Submitter(jobscript=jobscript, cluster_cmds=cluster_cmds)
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
        jobscript = argv[-1]
        cluster_cmds = argv[1:-1]
        lsf_submit = Submitter(
            jobscript=jobscript, cluster_cmds=cluster_cmds, memory_units=mem_units
        )

        lsf_submit.submit()

        expected_logdir = (
                Path("logdir") / lsf_submit.rule_name / lsf_submit.wildcards_str
        )
        mkdir_mock.assert_called_once_with(expected_logdir)
        self.assertEqual(remove_file_mock.call_count, 2)
        expected_outlog = expected_logdir / "jobid2_random.out"
        expected_errlog = expected_logdir / "jobid2_random.err"
        expected_jobinfo_cmd = '-o "{outlog}" -e "{errlog}" -J "search_fasta_on_index.i=0"'.format(
            outlog=expected_outlog, errlog=expected_errlog
        )
        remove_file_mock.assert_any_call(expected_outlog)
        remove_file_mock.assert_any_call(expected_errlog)
        expected_mem = "2662{}".format(mem_units.value)
        run_process_mock.assert_called_once_with(
            "bsub -M {mem} -n 1 -R 'select[mem>{mem}] rusage[mem={mem}] span[hosts=1]' "
            "{jobinfo} -q q1 cluster_opt_1 cluster_opt_2 cluster_opt_3 "
            "real_jobscript.sh".format(mem=expected_mem, jobinfo=expected_jobinfo_cmd)
        )
        print_mock.assert_called_once_with(
            "123456 {outlog}".format(outlog=expected_outlog)
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
        jobscript = argv[-1]
        cluster_cmds = argv[1:-1]
        lsf_submit = Submitter(jobscript=jobscript, cluster_cmds=cluster_cmds)

        self.assertRaises(BsubInvocationError, lsf_submit.submit)

        expected_logdir = (
            Path("logdir") / lsf_submit.rule_name / lsf_submit.wildcards_str
        )
        mkdir_mock.assert_called_once_with(expected_logdir)
        self.assertEqual(remove_file_mock.call_count, 2)
        expected_outlog = expected_logdir / "jobid2_random.out"
        expected_errlog = expected_logdir / "jobid2_random.err"
        expected_jobinfo_cmd = '-o "{outlog}" -e "{errlog}" -J "search_fasta_on_index.i=0"'.format(
            outlog=expected_outlog, errlog=expected_errlog
        )
        remove_file_mock.assert_any_call(expected_outlog)
        remove_file_mock.assert_any_call(expected_errlog)
        expected_mem = "2662KB"
        run_process_mock.assert_called_once_with(
            "bsub -M {mem} -n 1 -R 'select[mem>{mem}] rusage[mem={mem}] span[hosts=1]' "
            "{jobinfo} -q q1 cluster_opt_1 cluster_opt_2 cluster_opt_3 "
            "real_jobscript.sh".format(mem=expected_mem, jobinfo=expected_jobinfo_cmd)
        )
        print_mock.assert_not_called()

    @patch.object(
        CookieCutter, CookieCutter.get_default_queue.__name__, return_value="queue"
    )
    def test_get_queue_cmd_returns_cookiecutter_default_if_no_cluster_config(
        self, *mock
    ):
        argv = [
            "script_name",
            "cluster_opt_1",
            "cluster_opt_2",
            "cluster_opt_3",
            "real_jobscript.sh",
        ]
        jobscript = argv[-1]
        cluster_cmds = argv[1:-1]
        lsf_submit = Submitter(jobscript=jobscript, cluster_cmds=cluster_cmds)
        # sorry, this is hacky but I couldn't figure out how to mock read_job_properties
        del lsf_submit._job_properties["cluster"]

        actual = lsf_submit.queue_cmd
        expected = "-q queue"

        self.assertEqual(actual, expected)

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
    def test_rule_specific_params_are_submitted(self, *mocks):
        argv = [
            "script_name",
            "cluster_opt_1",
            "cluster_opt_2",
            "cluster_opt_3",
            "real_jobscript.sh",
        ]
        stream = StringIO(
            "__default__:\n  - '-q queue'\n  - '-gpu -'\nsearch_fasta_on_index: '-P project'"
        )
        lsf_config = Config.from_stream(stream)
        memory_units = MemoryUnits.GB
        jobscript = argv[-1]
        cluster_cmds = argv[1:-1]
        lsf_submit = Submitter(
            jobscript=jobscript,
            cluster_cmds=cluster_cmds,
            memory_units=memory_units,
            lsf_config=lsf_config,
        )

        actual = lsf_submit.submit_cmd
        print(actual)
        expected_mem = "2662{}".format(memory_units.value)
        expected_outlog = (
            Path("logdir") / "search_fasta_on_index" / "i=0" / "jobid2_random.out"
        )
        expected_errlog = (
            Path("logdir") / "search_fasta_on_index" / "i=0" / "jobid2_random.err"
        )
        expected_jobinfo_cmd = '-o "{outlog}" -e "{errlog}" -J "search_fasta_on_index.i=0"'.format(
            outlog=expected_outlog, errlog=expected_errlog
        )
        expected = (
            "bsub -M {mem} -n 1 -R 'select[mem>{mem}] rusage[mem={mem}] span[hosts=1]' "
            "{jobinfo} -q q1 cluster_opt_1 cluster_opt_2 cluster_opt_3 "
            "-q queue -gpu - -P project "
            "real_jobscript.sh".format(mem=expected_mem, jobinfo=expected_jobinfo_cmd)
        )
        print(expected)

        assert actual == expected


if __name__ == "__main__":
    unittest.main()
