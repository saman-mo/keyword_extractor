import pytest

from ai_es_utils.queries.components import MonthsWorkingQuery
from ai_es_utils.queries.models.payload import RequestPayload, Query
from tests.utils import load_base_query

target_query_body = load_base_query("months_working_query.json")
target_query_body_only_min = load_base_query("months_working_query_only_min.json")
target_query_body_only_max = load_base_query("months_working_query_only_max.json")


@pytest.mark.parametrize(
    "years_working_min, years_working_max, _target_query_body", [
        (1, 3, target_query_body),
        (1, None, target_query_body_only_min),
        (None, 3, target_query_body_only_max),
        (None, None, {})
    ]
)
def test_base_query(years_working_min: int, years_working_max: int, _target_query_body: dict):
    _query = MonthsWorkingQuery()

    payload = RequestPayload()
    if years_working_min is not None or years_working_max is not None:
        payload = RequestPayload(
            query=Query(
                yearsWorkingMin=years_working_min,
                yearsWorkingMax=years_working_max
            )
        )

    assert _query.query(payload).query == _target_query_body
