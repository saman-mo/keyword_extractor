from typing import List

import pytest

from ai_es_utils.queries.components import WorksAtQuery
from ai_es_utils.queries.models.payload import RequestPayload, Query
from tests.utils import load_base_query

target_query_body = load_base_query("works_at_query.json")
target_query_body_multiple_tokens = load_base_query("works_at_query_multiple_tokens.json")


@pytest.mark.parametrize(
    "works_at, _target_query_body", [
        (["google", "facebook"], target_query_body),
        (["google gmbh", "Wow so cool company gmbh inc"], target_query_body_multiple_tokens),
        (None, {})
    ]
)
def test_base_query(works_at: List[str], _target_query_body: dict):
    _query = WorksAtQuery()

    payload = RequestPayload()
    if works_at is not None:
        payload = RequestPayload(
            query=Query(worksAt=works_at)
        )

    assert _query.query(payload).query == _target_query_body
