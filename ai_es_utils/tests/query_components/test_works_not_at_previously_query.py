from typing import List

import pytest

from ai_es_utils.queries.components import WorksNotAtPreviouslyQuery
from ai_es_utils.queries.models.payload import RequestPayload, Query
from tests.utils import load_base_query

target_query_body_multiple_tokens = load_base_query("works_not_at_previously_query_multiple_tokens.json")


@pytest.mark.parametrize(
    "previously_at_exclude, _target_query_body", [
        (["google gmbh", "Wow so cool company gmbh inc"], target_query_body_multiple_tokens),
        (None, {})
    ]
)
def test_base_query(previously_at_exclude: List[str], _target_query_body: dict):
    _query = WorksNotAtPreviouslyQuery()

    payload = RequestPayload()
    if previously_at_exclude is not None:
        payload = RequestPayload(
            query=Query(previouslyAtExclude=previously_at_exclude)
        )

    assert _query.query(payload).query == _target_query_body
