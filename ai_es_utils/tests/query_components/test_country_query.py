import pytest

from ai_es_utils.queries.components import CountryQuery
from ai_es_utils.queries.models.payload import RequestPayload, Query
from ai_es_utils.queries.models.country import Country
from tests.utils import load_base_query, load_json_from_test_data

target_query_body = load_base_query("country_query.json")
target_query_body_country_not_in_map = load_base_query("country_query_not_in_map.json")
target_query_body_country_value_not_given = load_base_query("country_query_country_value_not_given.json")
country_map = load_json_from_test_data("country_names_map.json")


@pytest.mark.parametrize(
    "country, _target_query_body", [
        ({"text": "Deutschland", "value": "DE"}, target_query_body),
        ({"text": "DoesNotExist", "value": "XX"}, target_query_body_country_not_in_map),
        # Incomplete country data
        ({"value": "DE"}, target_query_body),
        ({"text": "DoesNotExist"}, target_query_body_country_value_not_given),
        (None, {})
    ]
)
def test_base_query(country: dict, _target_query_body: dict):
    _query = CountryQuery(country_names=country_map)

    payload = RequestPayload()
    if country is not None:
        payload = RequestPayload(
            query=Query(country=Country(**country))
        )

    assert _query.query(payload).query == _target_query_body


@pytest.mark.parametrize(
    "country, _target_query_body", [
        ({"text": "Deutschland", "value": "DE"}, target_query_body),
        ({"text": "DoesNotExist", "value": "XX"}, target_query_body_country_not_in_map),
        # Incomplete country data
        ({"value": "DE"}, target_query_body),
        ({"text": "DoesNotExist"}, target_query_body_country_value_not_given),
        (None, {})
    ]
)
def test_dict_formatted_query(country: dict, _target_query_body: dict):
    _query = CountryQuery(country_names=country_map)

    payload = RequestPayload()
    if country is not None:
        payload = RequestPayload(
            query=Query(country=country)
        )

    assert _query.query(payload).query == _target_query_body
