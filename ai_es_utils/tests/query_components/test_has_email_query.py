import pytest

from ai_es_utils.queries.components import HasEmailQuery
from ai_es_utils.queries.models.payload import RequestPayload, Query
from tests.utils import load_base_query

target_query_body_is_scientist = load_base_query("has_email_query_true.json")
target_query_body_is_not_scientist = load_base_query("has_email_query_false.json")


@pytest.mark.parametrize(
    "has_email, _target_query_body", [
        (True, target_query_body_is_scientist),
        (False, target_query_body_is_not_scientist),
        (None, {})
    ]
)
def test_base_query(has_email: bool, _target_query_body: dict):
    _query = HasEmailQuery()

    payload = RequestPayload()
    if has_email is not None:
        payload = RequestPayload(
            query=Query(hasEmail=has_email)
        )

    assert _query.query(payload).query == _target_query_body
