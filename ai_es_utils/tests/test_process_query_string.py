import pytest

from ai_es_utils.queries.utils import escape_reserved_characters, build_query_string_phrase, generate_query_string


@pytest.mark.parametrize(
    "input_str, escaped_str", [
        ("manager (sales)", "manager \\(sales\\)"),
        ("manager [sales]", "manager \\[sales\\]"),
        ("sales/area manager", "sales\\/area manager"),
        ("java + web developer", "java \\+ web developer"),
        ("data-scientist", "data\\-scientist"),
        ("Novelity*\\Innovation^ }> Expert!? <{", "Novelity\\*\\\\Innovation\\^ \\}\\> Expert\\!\\? \\<\\{"),
        ('"Special": Snowflake~', '\\"Special\\"\\: Snowflake\\~')
    ]
)
def test_escape_special_characters(input_str, escaped_str):
    assert escape_reserved_characters(input_str) == escaped_str


@pytest.mark.parametrize(
    "input_str, expected_str, fuzzy", [
        ("area sales manager", "(area~ sales~ manager~)", True),
        ("area sales manager", "(area sales manager)", False)
    ]
)
def test_build_query_string_phrase(input_str, expected_str, fuzzy):
    assert build_query_string_phrase(input_str, fuzzy=fuzzy) == expected_str


@pytest.mark.parametrize(
    "term_list, expected_str", [
        (["sales manager", "area sales manager", "sales-manager"],
         "(sales~ manager~) OR (area~ sales~ manager~) OR (sales\\-manager~)")
    ]
)
def test_generate_query_string(term_list, expected_str):
    assert generate_query_string(term_list) == expected_str
