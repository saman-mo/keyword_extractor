import pytest

from ai_es_utils.queries.components import SkillExpansionQuery
from ai_es_utils.queries.models.payload import RequestPayload, Query
from ai_es_utils.queries.models.query import SemanticExpansion
from tests.utils import load_base_query, load_json_from_test_data
from .mocking.mock_job2skills_service import MockJob2SkillsService

target_query_body_developer = load_base_query("skill_expansion_query.json")
target_query_body_developer_nested = load_base_query("skill_expansion_query_nested.json")
target_query_body_curated_developer = load_base_query("skill_expansion_query_curated_developer.json")
target_query_body_curated_bankkauffrau = load_base_query("skill_expansion_query_curated_bankkauffrau.json")

gender_normalization_map = load_json_from_test_data("gender_normalization_map.json")

job2skills_mock_data = load_json_from_test_data("mock_job2skills_data.json")
job2skills_service = MockJob2SkillsService(job2skills_mock_data)

semantic_expansion_developer = SemanticExpansion(**load_json_from_test_data("mock_semantic_expansion_developer.json"))

semantic_expansion_developer_all_checked = SemanticExpansion(**load_json_from_test_data("mock_semantic_expansion_developer.json"))
semantic_expansion_developer_all_checked.skills[0]["isChecked"] = True
semantic_expansion_developer_all_checked.skills[1]["isChecked"] = True

curated_skills_expansions = load_json_from_test_data("curated_skills_expansions.json")

skill_expansion_query = SkillExpansionQuery(
    job2skills_service,
    boosted_fields=["skills^3.0", "jobTitle^2.0", "previousJobTitles", "jobs.notes^0.5"],
    gender_normalization_map=gender_normalization_map,
    curated_skills_expansion=curated_skills_expansions
)


@pytest.mark.parametrize(
    "job_title, nested_bool, _target_query_body", [
        ("developer", False, target_query_body_developer),
        ("developer", True, target_query_body_developer_nested),
        ("unknown or empty", True, {}),
        (None, False, {})
    ]
)
def test_base_query(job_title: str, nested_bool: bool, _target_query_body: dict):
    _skill_expansion_query = SkillExpansionQuery(
        job2skills_service,
        boosted_fields=["skills^3.0", "jobTitle^2.0", "previousJobTitles", "jobs.notes^0.5"],
        gender_normalization_map=gender_normalization_map,
        curated_skills_expansion=curated_skills_expansions,
        nested_bool=nested_bool
    )

    payload = RequestPayload()
    if job_title is not None:
        payload = RequestPayload(
            query=Query(jobTitle=job_title)
        )

    assert _skill_expansion_query.query(payload, "valid token").query == _target_query_body


@pytest.mark.parametrize(
    "token, _target_query_body", [
        ("valid token", target_query_body_developer),
        ("invalid token", {}),
        (None, {})
    ]
)
def test_authorization(token: str, _target_query_body: dict):
    payload = RequestPayload(query=Query(jobTitle="developer"))
    assert skill_expansion_query.query(payload, token).query == _target_query_body


@pytest.mark.parametrize(
    "job_title, semantic_expansion, _target_query_body", [
        ("developer", None, target_query_body_developer),
        ("developer", semantic_expansion_developer, target_query_body_curated_developer),
        ("bankkauffrau", None, target_query_body_curated_bankkauffrau)
    ]
)
def test_curated_semantic_expansion(job_title: str, semantic_expansion: SemanticExpansion, _target_query_body: dict):
    payload = RequestPayload(
        query=Query(
            jobTitle=job_title,
            semanticExpansion=semantic_expansion
        )
    )

    assert skill_expansion_query.query(payload, "valid token").query == _target_query_body


@pytest.mark.parametrize(
    "job_title, semantic_expansion, target_semantic_expansion", [
        # First search, no expansion provided
        ("developer", None, semantic_expansion_developer_all_checked),
        # Expansion provided, but only for jobs
        ("developer",
         SemanticExpansion(jobs=[{"name": "stuff", "isChecked": True}], skills=None),
         semantic_expansion_developer_all_checked),
        # Valid expansion provided
        ("developer", semantic_expansion_developer, semantic_expansion_developer)
    ]
)
def test_semantic_expansion_response(job_title: str, semantic_expansion: SemanticExpansion,
                                     target_semantic_expansion: SemanticExpansion):
    payload = RequestPayload(
        query=Query(
            jobTitle=job_title,
            semanticExpansion=semantic_expansion
        )
    )

    response_data = skill_expansion_query.query(payload, "valid token").response_data

    assert response_data["semanticExpansion"]["skills"] == target_semantic_expansion.skills
