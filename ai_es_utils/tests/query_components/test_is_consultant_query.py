import pytest

from ai_es_utils.queries.components import IsConsultantQuery
from ai_es_utils.queries.models.payload import RequestPayload, Query
from tests.utils import load_base_query

target_query_body_is_consultant = load_base_query("is_consultant_query_true.json")
target_query_body_is_not_consultant = load_base_query("is_consultant_query_false.json")


@pytest.mark.parametrize(
    "consultants_only, _target_query_body", [
        (True, target_query_body_is_consultant),
        (False, target_query_body_is_not_consultant),
        (None, {})
    ]
)
def test_base_query(consultants_only: bool, _target_query_body: dict):
    _query = IsConsultantQuery()

    payload = RequestPayload()
    if consultants_only is not None:
        payload = RequestPayload(
            query=Query(consultantsOnly=consultants_only)
        )

    assert _query.query(payload).query == _target_query_body
