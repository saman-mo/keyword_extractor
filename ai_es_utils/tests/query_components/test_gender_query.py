import pytest

from ai_es_utils.queries.components import GenderQuery
from ai_es_utils.queries.models.payload import RequestPayload, Query
from tests.utils import load_base_query

target_male_query_body = load_base_query("match_gender_query_male.json")
target_female_query_body = load_base_query("match_gender_query_female.json")


@pytest.mark.parametrize(
    "is_male, _target_query_body", [
        (True, target_male_query_body),
        (False, target_female_query_body),
        (None, {})
    ]
)
def test_base_query(is_male: bool, _target_query_body: dict):
    match_gender_query = GenderQuery()

    payload = RequestPayload()
    if is_male is not None:
        payload = RequestPayload(
            query=Query(isMale=is_male)
        )

    assert match_gender_query.query(payload).query == _target_query_body
