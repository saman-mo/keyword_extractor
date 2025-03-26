import pytest

from ai_es_utils.queries.components import HighlightQuery
from ai_es_utils.queries.models.payload import RequestPayload
from tests.utils import load_base_query

target_query_body_default = load_base_query("highlight_query.json")
target_query_body_fields = load_base_query("highlight_query.json")
target_query_body_fields["highlight"]["fields"] = {f: dict() for f in ["company", "email"]}


@pytest.mark.parametrize(
    "fields, _target_query_body", [
        (["company", "email"], target_query_body_fields),
        (None, target_query_body_default)
    ]
)
def test_base_query(fields, _target_query_body):
    _query = HighlightQuery()
    if fields is not None:
        _query = HighlightQuery(highlight_fields=fields)

    payload = RequestPayload()
    assert _query.query(payload).query == _target_query_body
