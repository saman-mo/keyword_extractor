import pytest

from ai_es_utils.queries.components import SizeAndOffsetQuery
from ai_es_utils.queries.models.payload import RequestPayload


@pytest.mark.parametrize(
    "offset, size, _target_query_body", [
        (10, 20, {"from": 10, "size": 20}),
        (10, None, {"from": 10, "size": 30}),
        (None, 10, {"from": 0, "size": 10}),
        (None, None, {"from": 0, "size": 30})
    ]
)
def test_base_query(offset, size, _target_query_body):
    _query = SizeAndOffsetQuery()

    filter_dict = {
        "size": size,
        "offset": offset
    }
    filter_dict = {k: v for k, v in filter_dict.items() if v is not None}

    payload = RequestPayload()
    if filter_dict:
        payload = RequestPayload(filter=filter_dict)

    assert _query.query(payload).query == _target_query_body
