import pytest

from ai_es_utils.queries.components import IndustryCodeQuery
from ai_es_utils.queries.models.payload import RequestPayload, Query
from tests.utils import load_base_query

target_query_body = load_base_query("industry_code_query.json")
target_query_body_nested = load_base_query("industry_code_query_nested.json")


@pytest.mark.parametrize(
    "industry_code, nested_bool, _target_query_body", [
        ("010", False, target_query_body),
        ("010", True, target_query_body_nested),
        (None, True, {}),
        (None, False, {})
    ]
)
def test_base_query(industry_code: str, nested_bool: bool, _target_query_body: dict):
    _query = IndustryCodeQuery(nested_bool=nested_bool)

    payload = RequestPayload()
    if industry_code is not None:
        payload = RequestPayload(
            query=Query(industryCode=industry_code)
        )

    assert _query.query(payload).query == _target_query_body
