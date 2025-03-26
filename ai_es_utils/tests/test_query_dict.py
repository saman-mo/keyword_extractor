import pytest

from typing import Dict, Any

from ai_es_utils.queries.utils import query_dict


@pytest.mark.parametrize(
    "base_key, input_dict, expected_dict", [
        ("ids", {"values": ["asdf"]}, {"ids": {"values": ["asdf"]}}),
        ("ids", {}, {"ids": {}})
    ]
)
def test_query_dict(base_key: str, input_dict: Dict[str, Any], expected_dict: Dict[str, Any]):
    assert query_dict(base_key, **input_dict) == expected_dict
