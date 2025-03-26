import json
import os

import pytest

from ai_es_utils.search.process_results import SearchResultProcessor
from .utils import add_pytest_cwd


def _load_search_result(file_name: str) -> dict:
    return json.load(open(add_pytest_cwd(os.path.join("test_data", "search_result", file_name))))


search_result = _load_search_result("full_search_result.json")
processor = SearchResultProcessor()


@pytest.mark.parametrize(
    "input_value, expected_value", [
        (62, 62),
        (10_000, 9_990),
        (0, 0)
    ]
)
def test_get_instance_count(input_value, expected_value):
    search_result["hits"]["total"] = input_value
    return_value = processor(search_result)["profileInstanceCount"]
    assert return_value == expected_value


@pytest.mark.parametrize(
    "input_value, expected_value", [
        (80, int(100 * 80 / 83.75648)),
        (0, 1)
    ]
)
def test_get_relevance_from_score(input_value, expected_value):
    processor(search_result)
    assert processor._get_relevance_from_score(input_value) == expected_value
