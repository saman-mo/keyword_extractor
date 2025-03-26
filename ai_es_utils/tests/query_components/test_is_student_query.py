import pytest

from ai_es_utils.queries.components import IsStudentQuery
from ai_es_utils.queries.models.payload import RequestPayload, Query
from tests.utils import load_base_query

target_query_body_is_student = load_base_query("is_student_query_true.json")
target_query_body_is_not_student = load_base_query("is_student_query_false.json")


@pytest.mark.parametrize(
    "students_only, _target_query_body", [
        (True, target_query_body_is_student),
        (False, target_query_body_is_not_student),
        (None, {})
    ]
)
def test_base_query(students_only: bool, _target_query_body: dict):
    _query = IsStudentQuery()

    payload = RequestPayload()
    if students_only is not None:
        payload = RequestPayload(
            query=Query(studentsOnly=students_only)
        )

    assert _query.query(payload).query == _target_query_body
