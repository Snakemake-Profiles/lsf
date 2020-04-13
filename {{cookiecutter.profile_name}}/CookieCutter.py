class CookieCutter:
    """
    Cookie Cutter wrapper
    """

    @staticmethod
    def get_default_threads() -> int:
        return int("{{cookiecutter.default_threads}}")

    @staticmethod
    def get_default_mem_mb() -> int:
        return int("{{cookiecutter.default_mem_mb}}")

    @staticmethod
    def get_log_dir() -> str:
        return "{{cookiecutter.default_cluster_logdir}}"

    @staticmethod
    def get_default_queue() -> str:
        return "{{cookiecutter.default_queue}}"

    @staticmethod
    def get_lsf_unit_for_limits() -> str:
        return "{{cookiecutter.LSF_UNIT_FOR_LIMITS}}"
