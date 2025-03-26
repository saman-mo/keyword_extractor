import pytest

from ai_es_utils.queries.components import JobTitleExpansionBooleanQuery
from ai_es_utils.queries.models.payload import RequestPayload, Query
from tests.utils import load_base_query, load_json_from_test_data
from .mocking.mock_job2jobs_service import MockJob2JobsService

target_query_body = load_base_query("job_title_expansion_boolean_query_entwicklerin.json")
target_query_body_nested = load_base_query("job_title_expansion_boolean_query_entwicklerin_nested.json")

gender_normalization_map = load_json_from_test_data("gender_normalization_map.json")

job2jobs_mock_data = load_json_from_test_data("mock_job2jobs_data.json")
job2jobs_service = MockJob2JobsService(job2jobs_mock_data)

curated_jobs_expansions = load_json_from_test_data("curated_jobs_expansions.json")


@pytest.mark.parametrize(
    "job_title, nested_bool, _target_query_body", [
        ("entwickler/in", False, target_query_body),
        ("Entwickler/in", False, target_query_body),
        ("entwickler/in", True, target_query_body_nested),
        (None, True, {}),
        (None, False, {})
    ]
)
def test_base_query(job_title: str, nested_bool: bool, _target_query_body: dict):
    job_title_expansion_query = JobTitleExpansionBooleanQuery(
        job2jobs_service,
        boosted_fields=["jobTitle^3.0", "previousJobTitles", "jobs.jobTitle^2.0", "jobs.notes^0.5"],
        gender_normalization_map=gender_normalization_map,
        curated_jobs_expansion=curated_jobs_expansions,
        nested_bool=nested_bool
    )

    payload = RequestPayload()
    if job_title is not None:
        payload = RequestPayload(
            query=Query(jobTitle=job_title)
        )

    assert job_title_expansion_query.query(payload, bearer_token="valid token").query == _target_query_body
