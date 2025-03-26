from typing import List

import pytest

from ai_es_utils.queries.components import IncludePortalsQuery
from ai_es_utils.queries.models.payload import RequestPayload, Query
from tests.utils import load_base_query

target_query_body = load_base_query("include_portals_query.json")


@pytest.mark.parametrize(
    "include_portals, _target_query_body", [
        (["network1", "network2", "network3"], target_query_body),
        ([], {}),
        (None, {})
    ]
)
def test_base_query(include_portals: List[str], _target_query_body: dict):
    exclude_portals_query = IncludePortalsQuery()

    payload = RequestPayload()
    if include_portals is not None:
        payload = RequestPayload(
            query=Query(includePortals=include_portals)
        )

    assert exclude_portals_query.query(payload).query == _target_query_body
