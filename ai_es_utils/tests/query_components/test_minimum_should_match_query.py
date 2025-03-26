import pytest

from ai_es_utils.queries.components import MinimumShouldMatchQuery
from ai_es_utils.queries.models.payload import RequestPayload
from tests.utils import load_base_query

target_query_body = load_base_query("minimum_should_match_query.json")


@pytest.mark.parametrize(
    "minimum_should_match, name, _target_query_body", [
        (1, "test", target_query_body)
    ]
)
def test_base_query(minimum_should_match, name, _target_query_body):
    _query = MinimumShouldMatchQuery(name=name, minimum_should_match=minimum_should_match)

    payload = RequestPayload()

    assert _query.query(payload).query == _target_query_body
