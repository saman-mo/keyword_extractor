from typing import List

import pytest

from ai_es_utils.queries.components import JobTitleExpansionMultiMatchQuery
from ai_es_utils.queries.models.payload import RequestPayload, Query
from ai_es_utils.queries.models.query import SemanticExpansion
from tests.utils import load_base_query, load_json_from_test_data
from .mocking.mock_job2jobs_service import MockJob2JobsService

target_query_body_developer = load_base_query("job_title_expansion_multi_match_query_developer.json")
target_query_body_curated_bankkauffrau = load_base_query("job_title_expansion_multi_match_query_curated_bankkauffrau.json")

gender_normalization_map = load_json_from_test_data("gender_normalization_map.json")

job2jobs_mock_data = load_json_from_test_data("mock_job2jobs_data.json")
job2jobs_service = MockJob2JobsService(job2jobs_mock_data)

semantic_expansion_developer = load_json_from_test_data("mock_semantic_expansion_developer.json")

semantic_expansion_developer_all_checked = load_json_from_test_data("mock_semantic_expansion_developer.json")
semantic_expansion_developer_all_checked["jobs"][0]["isChecked"] = True

curated_jobs_expansions = load_json_from_test_data("curated_jobs_expansions.json")

job_title_expansion_query = JobTitleExpansionMultiMatchQuery(
    job2jobs_service,
    gender_normalization_map=gender_normalization_map,
    curated_jobs_expansion=curated_jobs_expansions
)


@pytest.mark.parametrize(
    "job_title, _target_query_body", [
        ("developer", target_query_body_developer),
        ("Developer", target_query_body_developer),  # upper case
        ("unknown or empty", {}),
        (None, {})
    ]
)
def test_base_query(job_title: str, _target_query_body: dict):
    payload = RequestPayload()
    if job_title is not None:
        payload = RequestPayload(
            query=Query(jobTitle=job_title)
        )

    assert job_title_expansion_query.query(payload, "valid token").query == _target_query_body


@pytest.mark.parametrize(
    "token, _target_query_body", [
        ("valid token", target_query_body_developer),
        ("invalid token", {}),
        (None, {})
    ]
)
def test_authorization(token: str, _target_query_body: dict):
    payload = RequestPayload(query=Query(jobTitle="developer"))
    assert job_title_expansion_query.query(payload, token).query == _target_query_body


@pytest.mark.parametrize(
    "job_title, semantic_expansion, _target_query_body", [
        ("developer", None, target_query_body_developer),
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

    assert job_title_expansion_query.query(payload, "valid token").query == _target_query_body
