import pytest

from ai_es_utils.queries.components import ExecutiveOnlyQuery
from ai_es_utils.queries.models.payload import RequestPayload, Query
from tests.utils import load_base_query, load_json_from_test_data

true_base_query = load_base_query("executive_only_true_query.json")
false_base_query = load_base_query("executive_only_false_query.json")

true_base_query_nested = load_base_query("executive_only_true_query_nested.json")
false_base_query_nested = load_base_query("executive_only_false_query_nested.json")

mocking_executive_query = load_json_from_test_data("executive_query.json")


@pytest.mark.parametrize(
    "executive_only, _target_query_body", [
        (True, true_base_query),
        (False, false_base_query),
        (None, {})
    ]
)
def test_base_query(executive_only: bool, _target_query_body: dict):
    executive_only_query = ExecutiveOnlyQuery(curated_executive_sub_query=mocking_executive_query)

    payload = RequestPayload()
    if executive_only is not None:
        payload = RequestPayload(
            query=Query(executiveOnly=executive_only)
        )

    assert executive_only_query.query(payload).query == _target_query_body


@pytest.mark.parametrize(
    "executive_only, _target_query_body", [
        (True, true_base_query_nested),
        (False, false_base_query_nested),
        (None, {})
    ]
)
def test_nested_base_query(executive_only: bool, _target_query_body: dict):
    executive_only_query = ExecutiveOnlyQuery(curated_executive_sub_query=mocking_executive_query, nested_bool=True)

    payload = RequestPayload()
    if executive_only is not None:
        payload = RequestPayload(
            query=Query(executiveOnly=executive_only)
        )

    assert executive_only_query.query(payload).query == _target_query_body
