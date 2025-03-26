import pytest

from ai_es_utils.queries.utils import parse_boosted_fields, ParseBoostedFieldError


@pytest.mark.parametrize(
    "boosted_fields, expected_tuple", [
        (["field^1.0"], [("field", 1.0)]),
        (["field"], [("field", 1.0)]),
        (["oneField", "anotherField^2.0"], [("oneField", 1.0), ("anotherField", 2.0)])
    ]
)
def test_parsing(boosted_fields, expected_tuple):
    fields, boosts = parse_boosted_fields(boosted_fields)
    assert list(zip(fields, boosts)) == expected_tuple


@pytest.mark.parametrize(
    "boosted_fields", [
        (["field^1.0^adsf"]),
        (["field^asdf"])
    ]
)
def test_assert_invalid_fields(boosted_fields):
    with pytest.raises(ParseBoostedFieldError):
        _, _ = parse_boosted_fields(boosted_fields)
