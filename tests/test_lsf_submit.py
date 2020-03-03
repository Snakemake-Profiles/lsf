import unittest
from unittest.mock import patch
from tests.src.lsf_submit import LSF_Submit
from tests.src.CookieCutter import CookieCutter
from tests.src.OSLayer import OSLayer
from pathlib import Path
from subprocess import CalledProcessError


class Test_LSF_Submit(unittest.TestCase):
    @patch.object(CookieCutter, CookieCutter.get_log_dir.__name__, return_value="logdir")
    @patch.object(CookieCutter, CookieCutter.get_default_mem_mb.__name__, return_value=1000)
    @patch.object(CookieCutter, CookieCutter.get_default_threads.__name__, return_value=8)
    @patch.object(OSLayer, OSLayer.get_random_alphanumerical_string.__name__, return_value="random")
    def test___several_trivial_getter_methods(self, *mocks):
        argv=["script_name", "cluster_opt_1", "cluster_opt_2", "cluster_opt_3", "real_jobscript.sh"]
        lsf_submit = LSF_Submit(argv)
        self.assertEqual(lsf_submit.jobscript, "real_jobscript.sh")
        self.assertEqual(lsf_submit.cluster_cmd, "cluster_opt_1 cluster_opt_2 cluster_opt_3")
        self.assertEqual(lsf_submit.threads, 1)
        self.assertEqual(lsf_submit.mem_mb, 2662)
        self.assertEqual(lsf_submit.jobid, 2)
        self.assertEqual(lsf_submit.wildcards_str, "i=0")
        self.assertEqual(lsf_submit.rule_name, "bulk_search_fasta_in_an_index")
        self.assertEqual(lsf_submit.is_group_jobtype, False)
        self.assertEqual(lsf_submit.resources_cmd, "-M 2662 -n 1 -R 'select[mem>2662] rusage[mem=2662] span[hosts=1]'")
        self.assertEqual(lsf_submit.jobname, "bulk_search_fasta_in_an_index.i=0")
        self.assertEqual(lsf_submit.logdir, Path("logdir"))
        self.assertEqual(lsf_submit.outlog, Path("logdir")/"cluster_checkpoints/2_random.out")
        self.assertEqual(lsf_submit.errlog, Path("logdir")/"cluster_checkpoints/2_random.err")
        self.assertEqual(lsf_submit.jobinfo_cmd, '-o "logdir/cluster_checkpoints/2_random.out" -e "logdir/cluster_checkpoints/2_random.err" -J "bulk_search_fasta_in_an_index.i=0"')
        self.assertEqual(lsf_submit.queue_cmd, '-q q1')
        self.assertEqual(lsf_submit.submit_cmd, "bsub -M 2662 -n 1 -R 'select[mem>2662] rusage[mem=2662] span[hosts=1]' "
                                                "-o \"logdir/cluster_checkpoints/2_random.out\" -e \"logdir/cluster_checkpoints/2_random.err\" -J \"bulk_search_fasta_in_an_index.i=0\" "
                                                "-q q1 "
                                                "cluster_opt_1 cluster_opt_2 cluster_opt_3 "
                                                "real_jobscript.sh")

    @patch.object(CookieCutter, CookieCutter.get_log_dir.__name__, return_value="logdir")
    @patch.object(CookieCutter, CookieCutter.get_default_mem_mb.__name__, return_value=1000)
    @patch.object(CookieCutter, CookieCutter.get_default_threads.__name__, return_value=8)
    @patch.object(OSLayer, OSLayer.get_random_alphanumerical_string.__name__, return_value="random")
    @patch.object(OSLayer, OSLayer.mkdir.__name__)
    @patch.object(OSLayer, OSLayer.remove_file.__name__)
    @patch.object(OSLayer, OSLayer.run_process_and_get_output_and_error_stream.__name__, return_value=("123456", ""))
    @patch.object(OSLayer, OSLayer.print.__name__)
    def test___submit___successfull_submit(self,
                                           print_mock,
                                           run_process_and_get_output_and_error_stream_mock,
                                           remove_file_mock,
                                           mkdir_mock,
                                           *uninteresting_mocks):
        argv = ["script_name", "cluster_opt_1", "cluster_opt_2", "cluster_opt_3", "real_jobscript.sh"]
        lsf_submit = LSF_Submit(argv)

        lsf_submit.submit()

        mkdir_mock.assert_called_once_with(Path("logdir"))
        self.assertEqual(remove_file_mock.call_count, 2)
        remove_file_mock.assert_any_call(Path("logdir/cluster_checkpoints/2_random.out"))
        remove_file_mock.assert_any_call(Path("logdir/cluster_checkpoints/2_random.err"))
        run_process_and_get_output_and_error_stream_mock.assert_called_once_with(
            "bsub -M 2662 -n 1 -R 'select[mem>2662] rusage[mem=2662] span[hosts=1]' "
            "-o \"logdir/cluster_checkpoints/2_random.out\" -e \"logdir/cluster_checkpoints/2_random.err\" -J \"bulk_search_fasta_in_an_index.i=0\" "
            "-q q1 "
            "cluster_opt_1 cluster_opt_2 cluster_opt_3 "
            "real_jobscript.sh"
        )
        print_mock.assert_called_once_with("123456 logdir/cluster_checkpoints/2_random.out")

    @patch.object(CookieCutter, CookieCutter.get_log_dir.__name__, return_value="logdir")
    @patch.object(CookieCutter, CookieCutter.get_default_mem_mb.__name__, return_value=1000)
    @patch.object(CookieCutter, CookieCutter.get_default_threads.__name__, return_value=8)
    @patch.object(OSLayer, OSLayer.get_random_alphanumerical_string.__name__, return_value="random")
    @patch.object(OSLayer, OSLayer.mkdir.__name__)
    @patch.object(OSLayer, OSLayer.remove_file.__name__)
    @patch.object(OSLayer, OSLayer.run_process_and_get_output_and_error_stream.__name__, side_effect = CalledProcessError(1, "bsub"))
    @patch.object(OSLayer, OSLayer.print.__name__)
    def test___submit___failed_submit(self,
                                           print_mock,
                                           run_process_and_get_output_and_error_stream_mock,
                                           remove_file_mock,
                                           mkdir_mock,
                                           *uninteresting_mocks):
        argv = ["script_name", "cluster_opt_1", "cluster_opt_2", "cluster_opt_3", "real_jobscript.sh"]
        lsf_submit = LSF_Submit(argv)

        self.assertRaises(CalledProcessError, lsf_submit.submit)

        mkdir_mock.assert_called_once_with(Path("logdir"))
        self.assertEqual(remove_file_mock.call_count, 2)
        remove_file_mock.assert_any_call(Path("logdir/cluster_checkpoints/2_random.out"))
        remove_file_mock.assert_any_call(Path("logdir/cluster_checkpoints/2_random.err"))
        run_process_and_get_output_and_error_stream_mock.assert_called_once_with(
            "bsub -M 2662 -n 1 -R 'select[mem>2662] rusage[mem=2662] span[hosts=1]' "
            "-o \"logdir/cluster_checkpoints/2_random.out\" -e \"logdir/cluster_checkpoints/2_random.err\" -J \"bulk_search_fasta_in_an_index.i=0\" "
            "-q q1 "
            "cluster_opt_1 cluster_opt_2 cluster_opt_3 "
            "real_jobscript.sh"
        )
        print_mock.assert_not_called()

if __name__ == '__main__':
    unittest.main()