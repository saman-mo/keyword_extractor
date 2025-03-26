import pytest

from ai_es_utils.queries.components import IsEntrepreneurQuery
from ai_es_utils.queries.models.payload import RequestPayload, Query
from tests.utils import load_base_query

target_query_body_is_entrepreneur = load_base_query("is_entrepreneur_query_true.json")
target_query_body_is_not_entrepreneur = load_base_query("is_entrepreneur_query_false.json")


@pytest.mark.parametrize(
    "entrepreneurs_only, _target_query_body", [
        (True, target_query_body_is_entrepreneur),
        (False, target_query_body_is_not_entrepreneur),
        (None, {})
    ]
)
def test_base_query(entrepreneurs_only: bool, _target_query_body: dict):
    _query = IsEntrepreneurQuery()

    payload = RequestPayload()
    if entrepreneurs_only is not None:
        payload = RequestPayload(
            query=Query(entrepreneursOnly=entrepreneurs_only)
        )

    assert _query.query(payload).query == _target_query_body
