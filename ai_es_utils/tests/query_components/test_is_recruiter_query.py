import pytest

from ai_es_utils.queries.components import IsRecruiterQuery
from ai_es_utils.queries.models.payload import RequestPayload, Query
from tests.utils import load_base_query

target_query_body_is_recruiter = load_base_query("is_recruiter_query_true.json")
target_query_body_is_not_recruiter = load_base_query("is_recruiter_query_false.json")


@pytest.mark.parametrize(
    "recruiter_only, _target_query_body", [
        (True, target_query_body_is_recruiter),
        (False, target_query_body_is_not_recruiter),
        (None, {})
    ]
)
def test_base_query(recruiter_only: bool, _target_query_body: dict):
    _query = IsRecruiterQuery()

    payload = RequestPayload()
    if recruiter_only is not None:
        payload = RequestPayload(
            query=Query(recruiterOnly=recruiter_only)
        )

    assert _query.query(payload).query == _target_query_body
