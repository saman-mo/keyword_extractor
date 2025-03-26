import pytest

from ai_es_utils.queries.components import SortQuery
from ai_es_utils.queries.models.payload import RequestPayload, Filter


@pytest.mark.parametrize(
    "sort_key, order, _target_query_body", [
        ("relevance", "desc", {"sort": [{"_score": {"order": "desc"}}]}),
        ("expertise", "desc", {"sort": [{"_score": {"order": "desc"}, "expertise": {"order": "desc"}}]}),
        ("mobility", None, {"sort": [{"_score": {"order": "desc"}, "mobility": {"order": "desc"}}]}),
        (None, "asc", {"sort": [{"_score": {"order": "asc"}}]}),
        (None, None, {"sort": [{"_score": {"order": "desc"}}]})
    ]
)
def test_base_query(sort_key, order, _target_query_body):
    _query = SortQuery()
    if order is not None:
        _query = SortQuery(order=order)

    payload = RequestPayload()
    if sort_key is not None:
        payload = RequestPayload(
            filter=Filter(sort=sort_key)
        )

    assert _query.query(payload).query == _target_query_body
