from ai_es_utils.queries.components import HideInSearchQuery
from ai_es_utils.queries.models.payload import RequestPayload
from tests.utils import load_base_query

target_query_body = load_base_query("hide_in_search_query_true.json")


def test_base_query():
    _query = HideInSearchQuery()
    payload = RequestPayload()
    assert _query.query(payload).query == target_query_body
