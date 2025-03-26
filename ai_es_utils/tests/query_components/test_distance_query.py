import pytest

from ai_es_utils.queries.components import DistanceQuery
from ai_es_utils.queries.models.payload import RequestPayload, Query
from ai_es_utils.queries.models.country import Country
from tests.utils import load_base_query, load_json_from_test_data
from .mocking.mock_geolocation_service import MockGeoLocationService

target_query_body = load_base_query("distance_query.json")
target_query_body_distance_25 = load_base_query("distance_query_distance_default.json")

geolocation_mock_data = load_json_from_test_data("mock_geolocation_data.json")
geolocation_service = MockGeoLocationService(geolocation_mock_data)

distance_query = DistanceQuery(
    geolocation_service
)


@pytest.mark.parametrize(
    "location, country, distance, _target_query_body", [
        ("Berlin", {"text": "Germany", "value": "DE"}, 33, target_query_body),
        ("Berlin", None, 33, target_query_body),
        (None, {"text": "Germany", "value": "DE"}, 33, {}),
        ("Berlin", {"text": "Germany", "value": "DE"}, 25, target_query_body_distance_25),
        (None, None, 25, {}),
        ("Unknown Location", {"text": "Germany", "value": "DE"}, 33, {})
    ]
)
def test_base_query(location, country, distance, _target_query_body):
    payload = RequestPayload()

    query_kwargs = {
        "location": location,
        "country": Country(**country) if country else country,
        "distance": distance
    }
    query_kwargs = {k: v for k, v in query_kwargs.items() if v is not None}

    if query_kwargs:
        payload = RequestPayload(
            query=Query(**query_kwargs)
        )

    assert distance_query.query(payload).query == _target_query_body
