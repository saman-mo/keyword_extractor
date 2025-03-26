import pytest

from ai_es_utils.queries.components import IsFreelancerQuery
from ai_es_utils.queries.models.payload import RequestPayload, Query
from tests.utils import load_base_query

target_query_body_is_freelancer = load_base_query("is_freelancer_query_true.json")
target_query_body_is_not_freelancer = load_base_query("is_freelancer_query_false.json")


@pytest.mark.parametrize(
    "freelancer_only, _target_query_body", [
        (True, target_query_body_is_freelancer),
        (False, target_query_body_is_not_freelancer),
        (None, {})
    ]
)
def test_base_query(freelancer_only: bool, _target_query_body: dict):
    _query = IsFreelancerQuery()

    payload = RequestPayload()
    if freelancer_only is not None:
        payload = RequestPayload(
            query=Query(freelancerOnly=freelancer_only)
        )

    assert _query.query(payload).query == _target_query_body
