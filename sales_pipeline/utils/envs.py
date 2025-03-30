import os


def get_bool_env(var_name: str, default: str = "false") -> bool:
    return os.environ.get(var_name, default).strip().lower() == "true"
