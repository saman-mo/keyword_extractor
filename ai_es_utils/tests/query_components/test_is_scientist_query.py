import pytest

from ai_es_utils.queries.components import IsScientistQuery
from ai_es_utils.queries.models.payload import RequestPayload, Query
from tests.utils import load_base_query

target_query_body_is_scientist = load_base_query("is_scientist_query_true.json")
target_query_body_is_not_scientist = load_base_query("is_scientist_query_false.json")


@pytest.mark.parametrize(
    "scientists_only, _target_query_body", [
        (True, target_query_body_is_scientist),
        (False, target_query_body_is_not_scientist),
        (None, {})
    ]
)
def test_base_query(scientists_only: bool, _target_query_body: dict):
    _query = IsScientistQuery()

    payload = RequestPayload()
    if scientists_only is not None:
        payload = RequestPayload(
            query=Query(scientistsOnly=scientists_only)
        )

    assert _query.query(payload).query == _target_query_body
