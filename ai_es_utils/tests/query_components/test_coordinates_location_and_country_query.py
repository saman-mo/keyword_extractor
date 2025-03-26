import pytest

from ai_es_utils.queries.components import CoordinatesLocationAndCountryQuery
from ai_es_utils.queries.models.payload import RequestPayload, Query
from ai_es_utils.queries.models.country import Country
from tests.utils import load_base_query

target_query_body = load_base_query("coordinates_location_and_country_query.json")
target_query_body_only_location = load_base_query("coordinates_location_and_country_query_only_location.json")


@pytest.mark.parametrize(
    "location, country, _target_query_body", [
        ("Wismar", {"text": "Deutschland", "value": "DE"}, target_query_body),
        ("Bernau (bei Berlin)", None, target_query_body_only_location),
        (None, None, {})
    ]
)
def test_base_query(location, country, _target_query_body):
    _query = CoordinatesLocationAndCountryQuery(fuzzy=True)

    kwargs = {}
    if location:
        kwargs["location"] = location
    if country:
        kwargs["country"] = Country(**country)

    payload = RequestPayload(query=Query(**kwargs))
    assert _query.query(payload).query == _target_query_body


@pytest.mark.parametrize(
    "location, country, _target_query_body", [
        ("Wismar", {"text": "Deutschland", "value": "DE"}, target_query_body),
        ("Bernau (bei Berlin)", None, target_query_body_only_location),
        (None, None, {})
    ]
)
def test_dict_formatted_base_query(location, country, _target_query_body):
    _query = CoordinatesLocationAndCountryQuery(fuzzy=True)

    kwargs = {}
    if location:
        kwargs["location"] = location
    if country:
        kwargs["country"] = country

    payload = RequestPayload(query=Query(**kwargs))
    assert _query.query(payload).query == _target_query_body