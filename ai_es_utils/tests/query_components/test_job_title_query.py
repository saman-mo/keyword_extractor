from typing import List

import pytest

from ai_es_utils.queries.components import JobTitleQuery
from ai_es_utils.queries.models.payload import RequestPayload, Query
from tests.utils import load_base_query, load_json_from_test_data

target_query_body = load_base_query("job_title_query.json")
target_query_body_direktor = load_base_query("job_title_query_gender_expansion_direktor.json")
target_query_body_entwickler_in = load_base_query("job_title_query_gender_expansion_entwickler-in.json")
target_query_body_nested_fields = load_base_query("job_title_query_nested_field_entwickler-in.json")
target_query_body_not_nested_fields = load_base_query("job_title_query_not_nested_field_entwickler-in.json")

gender_normalization_map = load_json_from_test_data("gender_normalization_map.json")

job_title_query = JobTitleQuery(
    boosted_fields=["jobTitle^2.0", "previousJobTitles"],
    gender_normalization_map=gender_normalization_map
)


@pytest.mark.parametrize(
    "job_title, _target_query_body", [
        ("developer", target_query_body),
        ("Developer", target_query_body),  # upper case
        (None, {})
    ]
)
def test_base_query(job_title: str, _target_query_body: dict):
    payload = RequestPayload()
    if job_title is not None:
        payload = RequestPayload(
            query=Query(jobTitle=job_title)
        )

    assert job_title_query.query(payload).query == _target_query_body


@pytest.mark.parametrize(
    "input_job_title, expected_query_body", [
        ("developer", target_query_body),  # Does not exist in gender map
        ("direktor", target_query_body_direktor),  # specific to all
        ("entwickler/in", target_query_body_entwickler_in),  # neutral to all
        ("Entwickler/in", target_query_body_entwickler_in)  # upper case neutral to all
    ]
)
def test_gender_normalized_query(input_job_title: dict, expected_query_body: dict):
    payload = RequestPayload(
        query=Query(jobTitle=input_job_title)
    )
    assert job_title_query.query(payload).query == expected_query_body


@pytest.mark.parametrize(
    "input_job_title, nested_bool, boosted_fields, expected_query_body", [
        ("entwickler", True, ["jobs.notes^0.5"], target_query_body_nested_fields),
        ("entwickler", False, ["jobs.notes^0.5"], target_query_body_not_nested_fields)
    ]
)
def test_nested_fields(input_job_title: str, nested_bool, boosted_fields: List[str], expected_query_body: dict):
    job_title_query = JobTitleQuery(
        boosted_fields=boosted_fields,
        gender_normalization_map=gender_normalization_map,
        nested_bool=nested_bool
    )
    payload = RequestPayload(
        query=Query(jobTitle=input_job_title)
    )
    assert job_title_query.query(payload).query == expected_query_body
