import json
import tempfile
import unittest
from io import StringIO
from pathlib import Path
from subprocess import CalledProcessError
from unittest.mock import patch

from tests.src.CookieCutter import CookieCutter
from tests.src.OSLayer import OSLayer
from tests.src.lsf_config import Config
from tests.src.lsf_submit import (
    Submitter,
    BsubInvocationError,
    JobidNotFoundError,
)
from tests.src.memory_units import Unit, Memory


class TestSubmitter(unittest.TestCase):
    @patch.object(
        CookieCutter, CookieCutter.get_log_dir.__name__, return_value="logdir"
    )
    @patch.object(
        CookieCutter, CookieCutter.get_default_mem_mb.__name__, return_value=1000
    )
    @patch.object(
        CookieCutter, CookieCutter.get_default_project.__name__, return_value="proj"
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
        memory_units = Unit.KILO
        memory_mb_value = 2662
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
        self.assertEqual(lsf_submit.mem_mb, Memory(memory_mb_value, Unit.MEGA))
        self.assertEqual(lsf_submit.jobid, "2")
        expected_wildcards_str = "i=0"
        self.assertEqual(lsf_submit.wildcards_str, expected_wildcards_str)
        expected_rule_name = "search_fasta_on_index"
        self.assertEqual(lsf_submit.rule_name, expected_rule_name)
        self.assertEqual(lsf_submit.is_group_jobtype, False)
        expected_mem = "{}000".format(memory_mb_value)
        expected_resource_cmd = (
            "-M {mem} -n 1 -R 'select[mem>{mem}] rusage[mem={mem}] span[hosts=1]'"
        ).format(mem=expected_mem)
        self.assertEqual(lsf_submit.resources_cmd, expected_resource_cmd)
        self.assertEqual(lsf_submit.jobname, "search_fasta_on_index.i=0")
        expected_logdir = Path("logdir") / expected_rule_name / expected_wildcards_str
        self.assertEqual(lsf_submit.logdir, expected_logdir)
        expected_outlog = expected_logdir / "jobid2_random.out"
        self.assertEqual(lsf_submit.outlog, expected_outlog)
        expected_errlog = expected_logdir / "jobid2_random.err"
        self.assertEqual(lsf_submit.errlog, expected_errlog)
        expected_jobinfo_cmd = (
            '-o "{outlog}" -e "{errlog}" -J "search_fasta_on_index.i=0"'
        ).format(outlog=expected_outlog, errlog=expected_errlog)
        self.assertEqual(lsf_submit.jobinfo_cmd, expected_jobinfo_cmd)
        self.assertEqual(lsf_submit.queue_cmd, "-q q1")
        self.assertEqual(
            lsf_submit.submit_cmd,
            "bsub -M {mem} -n 1 -R 'select[mem>{mem}] rusage[mem={mem}] span[hosts=1]' "
            "{jobinfo} -q q1 -P proj cluster_opt_1 cluster_opt_2 cluster_opt_3 "
            "real_jobscript.sh".format(mem=expected_mem, jobinfo=expected_jobinfo_cmd),
        )

    @patch.object(
        OSLayer,
        OSLayer.run_process.__name__,
        return_value=(
            (
                "Job <8697223> is submitted to default queue <research-rh74>. "
                "logs/cluster/2_z137TAmCoQGdWHohm5m2zHH5EruIEJBcQoi.out"
            ),
            "",
        ),
    )
    @patch.object(
        CookieCutter, CookieCutter.get_log_dir.__name__, return_value="logdir"
    )
    @patch.object(
        CookieCutter, CookieCutter.get_default_mem_mb.__name__, return_value=1000
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
        CookieCutter, CookieCutter.get_default_project.__name__, return_value="proj"
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
        mem_units = Unit.MEGA
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
        expected_jobinfo_cmd = (
            '-o "{outlog}" -e "{errlog}" -J "search_fasta_on_index.i=0"'
        ).format(outlog=expected_outlog, errlog=expected_errlog)
        remove_file_mock.assert_any_call(expected_outlog)
        remove_file_mock.assert_any_call(expected_errlog)
        expected_mem = "2662"
        run_process_mock.assert_called_once_with(
            "bsub -M {mem} -n 1 -R 'select[mem>{mem}] rusage[mem={mem}] span[hosts=1]' "
            "{jobinfo} -q q1 -P proj cluster_opt_1 cluster_opt_2 cluster_opt_3 "
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
        CookieCutter, CookieCutter.get_default_project.__name__, return_value="proj"
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
        expected_jobinfo_cmd = (
            '-o "{outlog}" -e "{errlog}" -J "search_fasta_on_index.i=0"'
        ).format(outlog=expected_outlog, errlog=expected_errlog)
        remove_file_mock.assert_any_call(expected_outlog)
        remove_file_mock.assert_any_call(expected_errlog)
        expected_mem = "2662"
        run_process_mock.assert_called_once_with(
            "bsub -M {mem} -n 1 -R 'select[mem>{mem}] rusage[mem={mem}] span[hosts=1]' "
            "{jobinfo} -q q1 -P proj cluster_opt_1 cluster_opt_2 cluster_opt_3 "
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
    @patch.object(OSLayer, OSLayer.get_uuid4_string.__name__, return_value="random")
    def test_rule_specific_params_are_submitted(self, *mocks):
        argv = [
            "script_name",
            "cluster_opt_1",
            "cluster_opt_2",
            "cluster_opt_3",
            "real_jobscript.sh",
        ]
        content = """
__default__:
  - "-R 'select[mem>2000]'"
  - '-gpu -'
search_fasta_on_index: '-P project'
"""
        stream = StringIO(content)
        lsf_config = Config.from_stream(stream)
        memory_units = Unit.MEGA
        jobscript = argv[-1]
        cluster_cmds = argv[1:-1]
        lsf_submit = Submitter(
            jobscript=jobscript,
            cluster_cmds=cluster_cmds,
            memory_units=memory_units,
            lsf_config=lsf_config,
        )

        actual = lsf_submit.submit_cmd
        expected_mem = "2662"
        expected_outlog = (
            Path("logdir") / "search_fasta_on_index" / "i=0" / "jobid2_random.out"
        )
        expected_errlog = (
            Path("logdir") / "search_fasta_on_index" / "i=0" / "jobid2_random.err"
        )
        expected_jobinfo_cmd = (
            '-o "{outlog}" -e "{errlog}" -J "search_fasta_on_index.i=0"'
        ).format(outlog=expected_outlog, errlog=expected_errlog)
        expected = (
            "bsub -M {mem} -n 1 -R 'select[mem>{mem}] rusage[mem={mem}] span[hosts=1]' "
            "{jobinfo} -q q1 cluster_opt_1 cluster_opt_2 cluster_opt_3 "
            "-R 'select[mem>2000]' -gpu - -P project "
            "real_jobscript.sh".format(mem=expected_mem, jobinfo=expected_jobinfo_cmd)
        )

        assert actual == expected

    @patch.object(
        CookieCutter, CookieCutter.get_log_dir.__name__, return_value="logdir"
    )
    @patch.object(
        CookieCutter, CookieCutter.get_default_mem_mb.__name__, return_value=1000
    )
    @patch.object(
        CookieCutter, CookieCutter.get_default_project.__name__, return_value="proj"
    )
    @patch.object(OSLayer, OSLayer.get_uuid4_string.__name__, return_value="random")
    def test_lsf_mem_unit_is_kb_and_mem_mb_is_converted_accordingly(self, *mocks):
        argv = [
            "script_name",
            "cluster_opt_1",
            "cluster_opt_2",
            "cluster_opt_3",
            "real_jobscript.sh",
        ]
        content = (
            "__default__:\n  - '-q queue'\n  - '-gpu -'\n"
            "search_fasta_on_index: '-P project'"
        )
        stream = StringIO(content)
        lsf_config = Config.from_stream(stream)
        lsf_mem_unit = Unit.KILO
        jobscript = argv[-1]
        cluster_cmds = argv[1:-1]
        lsf_submit = Submitter(
            jobscript=jobscript,
            cluster_cmds=cluster_cmds,
            memory_units=lsf_mem_unit,
            lsf_config=lsf_config,
        )

        actual = lsf_submit.submit_cmd
        expected_mem = "2662000"
        expected_outlog = (
            Path("logdir") / "search_fasta_on_index" / "i=0" / "jobid2_random.out"
        )
        expected_errlog = (
            Path("logdir") / "search_fasta_on_index" / "i=0" / "jobid2_random.err"
        )
        expected_jobinfo_cmd = (
            '-o "{outlog}" -e "{errlog}" -J "search_fasta_on_index.i=0"'
        ).format(outlog=expected_outlog, errlog=expected_errlog)
        expected = (
            "bsub -M {mem} -n 1 -R 'select[mem>{mem}] rusage[mem={mem}] span[hosts=1]' "
            "{jobinfo} cluster_opt_1 cluster_opt_2 cluster_opt_3 "
            "-q queue -gpu - -P project "
            "real_jobscript.sh".format(mem=expected_mem, jobinfo=expected_jobinfo_cmd)
        )

        assert actual == expected

    @patch.object(
        CookieCutter, CookieCutter.get_log_dir.__name__, return_value="logdir"
    )
    @patch.object(
        CookieCutter, CookieCutter.get_default_project.__name__, return_value="proj"
    )
    @patch.object(
        CookieCutter, CookieCutter.get_default_mem_mb.__name__, return_value=1000
    )
    @patch.object(OSLayer, OSLayer.get_uuid4_string.__name__, return_value="random")
    def test_lsf_mem_unit_is_tb_and_mem_mb_is_converted_and_rounded_up_to_int(
        self, *mocks
    ):
        argv = [
            "script_name",
            "cluster_opt_1",
            "cluster_opt_2",
            "cluster_opt_3",
            "real_jobscript.sh",
        ]
        content = (
            "__default__:\n  - '-q queue'\n  - '-gpu -'\n"
            "search_fasta_on_index: '-P project'"
        )
        stream = StringIO(content)
        lsf_config = Config.from_stream(stream)
        lsf_mem_unit = Unit.TERA
        jobscript = argv[-1]
        cluster_cmds = argv[1:-1]
        lsf_submit = Submitter(
            jobscript=jobscript,
            cluster_cmds=cluster_cmds,
            memory_units=lsf_mem_unit,
            lsf_config=lsf_config,
        )

        actual = lsf_submit.submit_cmd
        expected_mem = "1"
        expected_outlog = (
            Path("logdir") / "search_fasta_on_index" / "i=0" / "jobid2_random.out"
        )
        expected_errlog = (
            Path("logdir") / "search_fasta_on_index" / "i=0" / "jobid2_random.err"
        )
        expected_jobinfo_cmd = (
            '-o "{outlog}" -e "{errlog}" -J "search_fasta_on_index.i=0"'
        ).format(outlog=expected_outlog, errlog=expected_errlog)
        expected = (
            "bsub -M {mem} -n 1 -R 'select[mem>{mem}] rusage[mem={mem}] span[hosts=1]' "
            "{jobinfo} cluster_opt_1 cluster_opt_2 cluster_opt_3 "
            "-q queue -gpu - -P project "
            "real_jobscript.sh".format(mem=expected_mem, jobinfo=expected_jobinfo_cmd)
        )

        assert actual == expected

    def test_rule_name_for_group_returns_groupid_instead(self):
        jobscript = Path(tempfile.NamedTemporaryFile(delete=False, suffix=".sh").name)
        properties = json.dumps(
            {
                "type": "group",
                "groupid": "mygroup",
                "jobid": "a9722c33-51ba-5ac4-9f17-bab04c68bc3d",
            }
        )
        script_content = "#!/bin/sh\n# properties = {}\necho something".format(
            properties
        )
        jobscript.write_text(script_content)
        lsf_submit = Submitter(jobscript=str(jobscript))

        actual = lsf_submit.rule_name
        expected = "mygroup"

        assert actual == expected

    def test_is_group_jobtype_when_group_is_present(self):
        jobscript = Path(tempfile.NamedTemporaryFile(delete=False, suffix=".sh").name)
        properties = json.dumps(
            {
                "type": "group",
                "groupid": "mygroup",
                "jobid": "a9722c33-51ba-5ac4-9f17-bab04c68bc3d",
            }
        )
        script_content = "#!/bin/sh\n# properties = {}\necho something".format(
            properties
        )
        jobscript.write_text(script_content)
        lsf_submit = Submitter(jobscript=str(jobscript))

        assert lsf_submit.is_group_jobtype

    def test_is_group_jobtype_when_group_is_not_present(self):
        jobscript = Path(tempfile.NamedTemporaryFile(delete=False, suffix=".sh").name)
        properties = json.dumps({"jobid": "a9722c33-51ba-5ac4-9f17-bab04c68bc3d"})
        script_content = "#!/bin/sh\n# properties = {}\necho something".format(
            properties
        )
        jobscript.write_text(script_content)
        lsf_submit = Submitter(jobscript=str(jobscript))

        assert not lsf_submit.is_group_jobtype

    def test_jobid_for_group_returns_first_segment_of_uuid(self):
        jobscript = Path(tempfile.NamedTemporaryFile(delete=False, suffix=".sh").name)
        properties = json.dumps(
            {
                "type": "group",
                "groupid": "mygroup",
                "jobid": "a9722c33-51ba-5ac4-9f17-bab04c68bc3d",
            }
        )
        script_content = "#!/bin/sh\n# properties = {}\necho something".format(
            properties
        )
        jobscript.write_text(script_content)
        lsf_submit = Submitter(jobscript=str(jobscript))

        actual = lsf_submit.jobid
        expected = "a9722c33"

        assert actual == expected

    def test_jobid_for_non_group_returns_job_number(self):
        jobscript = Path(tempfile.NamedTemporaryFile(delete=False, suffix=".sh").name)
        properties = json.dumps(
            {
                "type": "single",
                "rule": "search_fasta_on_index",
                "wildcards": {"i": "0"},
                "jobid": 2,
            }
        )
        script_content = "#!/bin/sh\n# properties = {}\necho something".format(
            properties
        )
        jobscript.write_text(script_content)
        lsf_submit = Submitter(jobscript=str(jobscript))

        actual = lsf_submit.jobid
        expected = "2"

        assert actual == expected

    def test_jobname_for_non_group(self):
        jobscript = Path(tempfile.NamedTemporaryFile(delete=False, suffix=".sh").name)
        properties = json.dumps(
            {"type": "single", "rule": "search", "wildcards": {"i": "0"}, "jobid": 2}
        )
        script_content = "#!/bin/sh\n# properties = {}\necho something".format(
            properties
        )
        jobscript.write_text(script_content)
        lsf_submit = Submitter(jobscript=str(jobscript))

        actual = lsf_submit.jobname
        expected = "search.i=0"

        assert actual == expected

    def test_jobname_for_group(self):
        jobscript = Path(tempfile.NamedTemporaryFile(delete=False, suffix=".sh").name)
        properties = json.dumps(
            {
                "type": "group",
                "groupid": "mygroup",
                "jobid": "a9722c33-51ba-5ac4-9f17-bab04c68bc3d",
            }
        )
        script_content = "#!/bin/sh\n# properties = {}\necho something".format(
            properties
        )
        jobscript.write_text(script_content)
        lsf_submit = Submitter(jobscript=str(jobscript))

        actual = lsf_submit.jobname
        expected = "mygroup_a9722c33"

        assert actual == expected

    @patch.object(
        CookieCutter, CookieCutter.get_default_mem_mb.__name__, return_value=1000
    )
    def test_time_resource_for_group(self, *mocks):
        for time_str in ("time", "runtime", "walltime", "time_min"):
            jobscript = Path(
                tempfile.NamedTemporaryFile(delete=False, suffix=".sh").name
            )
            properties = json.dumps({"resources": {time_str: 1}})
            script_content = "#!/bin/sh\n# properties = {}\n" "echo something".format(
                properties
            )
            jobscript.write_text(script_content)
            lsf_submit = Submitter(jobscript=str(jobscript))

            actual = lsf_submit.resources_cmd
            expected = (
                "-M 1000 -n 1 -R 'select[mem>1000] rusage[mem=1000] "
                "span[hosts=1]' -W 1"
            )

            assert actual == expected


if __name__ == "__main__":
    unittest.main()
