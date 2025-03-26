import pytest

from ai_es_utils.queries.components import JobTitleBooleanQuery
from ai_es_utils.queries.models.payload import RequestPayload, Query
from tests.utils import load_base_query, load_json_from_test_data

target_query_body = load_base_query("job_title_boolean_query.json")
target_query_body_nested = load_base_query("job_title_boolean_query_nested.json")

gender_normalization_map = load_json_from_test_data("gender_normalization_map.json")


@pytest.mark.parametrize(
    "job_title, nested_bool, _target_query_body", [
        ("entwickler/in", False, target_query_body),
        ("Entwickler/in", False, target_query_body),
        ("entwickler/in", True, target_query_body_nested),
        (None, False, {}),
        (None, True, {})
    ]
)
def test_base_query(job_title: str, nested_bool: bool, _target_query_body: dict):
    job_title_boolean_query = JobTitleBooleanQuery(
        boosted_fields=["jobTitle^3.0", "previousJobTitles", "jobs.jobTitle^2.0", "jobs.notes^0.5"],
        gender_normalization_map=gender_normalization_map,
        nested_bool=nested_bool
    )

    payload = RequestPayload()
    if job_title is not None:
        payload = RequestPayload(
            query=Query(jobTitle=job_title)
        )

    assert job_title_boolean_query.query(payload).query == _target_query_body
