from typing import List

import pytest

from ai_es_utils.queries.components import WorksAtPreviouslyQuery
from ai_es_utils.queries.models.payload import RequestPayload, Query
from tests.utils import load_base_query

target_query_body_multiple_tokens = load_base_query("works_at_previously_query_multiple_tokens.json")


@pytest.mark.parametrize(
    "previously_at, _target_query_body", [
        (["google gmbh", "Wow so cool company gmbh inc"], target_query_body_multiple_tokens),
        (None, {})
    ]
)
def test_base_query(previously_at: List[str], _target_query_body: dict):
    _query = WorksAtPreviouslyQuery()

    payload = RequestPayload()
    if previously_at is not None:
        payload = RequestPayload(
            query=Query(previouslyAt=previously_at)
        )

    assert _query.query(payload).query == _target_query_body
