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
