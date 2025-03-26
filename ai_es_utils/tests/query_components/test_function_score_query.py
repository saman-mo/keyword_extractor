from ai_es_utils.queries.components import FunctionScoreQuery
from ai_es_utils.queries.models.payload import RequestPayload
from tests.utils import load_base_query

target_query_body = load_base_query("function_score_query.json")


def test_base_query():
    _query = FunctionScoreQuery()
    payload = RequestPayload()
    assert _query.query(payload).query == target_query_body
