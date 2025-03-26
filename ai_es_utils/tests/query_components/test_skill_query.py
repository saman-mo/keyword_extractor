from typing import List

import pytest

from ai_es_utils.queries.components import SkillQuery
from ai_es_utils.queries.models.payload import RequestPayload, Query
from tests.utils import load_base_query

target_query_body = load_base_query("skill_query.json")
target_query_body_nested = load_base_query("skill_query_nested_boosted_fields.json")
target_query_body_not_nested = load_base_query("skill_query_not_nested_boosted_fields.json")


@pytest.mark.parametrize(
    "skills, _target_query_body", [
        (["clean", "juggling"], target_query_body),
        ([], {}),
        (None, {})
    ]
)
def test_base_query(skills: List[str], _target_query_body: dict):
    skill_query = SkillQuery(boosted_fields=["skills^2.0", "jobTitle^0.5"])

    payload = RequestPayload()
    if skills is not None:
        payload = RequestPayload(
            query=Query(skills=skills)
        )

    assert skill_query.query(payload).query == _target_query_body


@pytest.mark.parametrize(
    "skills, nested_bool, _target_query_body", [
        (["clean", "juggling"], True, target_query_body_nested),
        (["clean", "juggling"], False, target_query_body_not_nested),
        ([], True, {}),
        (None, False, {})
    ]
)
def test_nested_fields(skills: List[str], nested_bool: bool, _target_query_body: dict):
    skill_query = SkillQuery(boosted_fields=["jobs.skills^2.0"], nested_bool=nested_bool)

    payload = RequestPayload()
    if skills is not None:
        payload = RequestPayload(
            query=Query(skills=skills)
        )

    assert skill_query.query(payload).query == _target_query_body
