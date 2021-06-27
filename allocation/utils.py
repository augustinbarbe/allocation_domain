from uuid import UUID
import importlib


def validate_uuid4(uuid_string):
    """
    Verify if the provided string is a uuid4
    return True or False
    """
    try:
        val = UUID(uuid_string, version=4)
    except ValueError:
        return False

    return val.hex == uuid_string.replace("-", "")


def load_config(file_path: str):
    """Helper to load config file as module"""
    spec = importlib.util.spec_from_file_location("config", file_path)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
    return config
