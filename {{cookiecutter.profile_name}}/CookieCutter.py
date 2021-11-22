class CookieCutter:
    """
    Cookie Cutter wrapper
    """

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
    def get_default_project() -> str:
        return int("{{cookiecutter.default_project}}")

    @staticmethod
    def get_lsf_unit_for_limits() -> str:
        return "{{cookiecutter.LSF_UNIT_FOR_LIMITS}}"

    @staticmethod
    def get_unknwn_behaviour() -> str:
        return "{{cookiecutter.UNKWN_behaviour}}"

    @staticmethod
    def get_zombi_behaviour() -> str:
        return "{{cookiecutter.ZOMBI_behaviour}}"

    @staticmethod
    def get_latency_wait() -> float:
        return float("{{cookiecutter.latency_wait}}")
