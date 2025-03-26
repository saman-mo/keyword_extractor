import pytest

from ai_es_utils.queries.components import HasPhoneQuery
from ai_es_utils.queries.models.payload import RequestPayload, Query
from tests.utils import load_base_query

target_query_body_is_scientist = load_base_query("has_phone_query_true.json")
target_query_body_is_not_scientist = load_base_query("has_phone_query_false.json")


@pytest.mark.parametrize(
    "has_phone, _target_query_body", [
        (True, target_query_body_is_scientist),
        (False, target_query_body_is_not_scientist),
        (None, {})
    ]
)
def test_base_query(has_phone: bool, _target_query_body: dict):
    _query = HasPhoneQuery()

    payload = RequestPayload()
    if has_phone is not None:
        payload = RequestPayload(
            query=Query(hasPhone=has_phone)
        )

    assert _query.query(payload).query == _target_query_body
