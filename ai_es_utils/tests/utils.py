import json
import os


def add_pytest_cwd(path: str) -> str:
    current_abs_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_abs_dir, path)


def load_base_query(file_name: str) -> dict:
    return json.load(
        open(add_pytest_cwd(
            os.path.join("query_components", "base_target_queries", file_name)
        ))
    )


def load_json_from_test_data(file_path: str):
    return json.load(open(add_pytest_cwd(os.path.join("query_components", "test_data", file_path))))


def load_json_from_test_root(file_path: str):
    return json.load(open(add_pytest_cwd(file_path)))
