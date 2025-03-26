import pytest

from ai_es_utils.queries.components import LanguagesQuery
from ai_es_utils.queries.models.payload import RequestPayload, Query
from tests.utils import load_base_query

target_query_body = load_base_query("languages_query.json")

_query = LanguagesQuery(boost=0.5)


@pytest.mark.parametrize(
    "languages, _target_query_body", [
        (["german", "english"], target_query_body),
        ([], {}),
        (None, {})
    ]
)
def test_base_query(languages: bool, _target_query_body: dict):
    payload = RequestPayload()
    if languages is not None:
        payload = RequestPayload(
            query=Query(languages=languages)
        )

    assert _query.query(payload).query == _target_query_body
