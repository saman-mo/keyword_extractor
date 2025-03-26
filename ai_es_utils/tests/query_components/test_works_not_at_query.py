from typing import List

import pytest

from ai_es_utils.queries.components import WorksNotAtQuery
from ai_es_utils.queries.models.payload import RequestPayload, Query
from tests.utils import load_base_query

target_query_body = load_base_query("works_not_at_query_multiple_tokens.json")


@pytest.mark.parametrize(
    "works_at_exclude, _target_query_body", [
        (["google gmbh", "Wow so cool company gmbh inc"], target_query_body),
        (None, {})
    ]
)
def test_base_query(works_at_exclude: List[str], _target_query_body: dict):
    _query = WorksNotAtQuery()

    payload = RequestPayload()
    if works_at_exclude is not None:
        payload = RequestPayload(
            query=Query(worksAtExclude=works_at_exclude)
        )

    assert _query.query(payload).query == _target_query_body
