import json
import pytest

from tests.utils import load_base_query
from ai_es_utils.queries.components import BlockingListQuery
from ai_es_utils.queries.models.payload import RequestPayload, Query

target_query_body = load_base_query("blocking_list_query.json")


@pytest.mark.parametrize(
    "blocklist, _target_query_body", [
        (["a", "b", "c"], target_query_body),
        (None, {})
    ]
)
def test_base_query(blocklist, _target_query_body):
    _query = BlockingListQuery()

    payload = RequestPayload()
    if blocklist is not None:
        payload = RequestPayload(
            query=Query(blocklist=blocklist)
        )
    assert _query.query(payload).query == _target_query_body
